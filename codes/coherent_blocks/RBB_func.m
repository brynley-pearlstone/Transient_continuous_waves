function [  data,sorted_binaries, sorted_odds_all, sorted_n_CP , sorted_evidence, P_gamma, sorted_priors, sanity_check, noise_settings, seg_settings] = RBB_func(n_chunks, signal_type, h_prior, chunk_SNR , mode, CP_prior, noise_seed, seg_seed)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here

% This script is to find the probability of obtaining any one of the 256
% 8-bit binary unmbers which could constitute a changepoint configuration.
% We define \Gamma as the 8 bit number, and \gamma_i as each bimary element
% of \Gamma.
% We can define the probability of \gamma_i as
% P_gamma = (1/(((2*pi)^-0.5)*sigma))*exp((-(D-gamma_i*h)^2)/(2*sigma^2));
% Now we can define some other things. for example, D is fed forward from
% the CW analysis. Sigmma may be given (look into feed forward from CW
% analysis), h fed forward from CW analysis
% We compute the probability for each of the 256 8-bit numbers

h_sd = 1*10^(-24);
h =  0.8* h_sd;
sigma = h /chunk_SNR;
hs = linspace(0, h_sd, 1001);
[offset, h_loc] = min(abs(hs - h));

if strcmp(h_prior, 'delta')
     l_prior = log(zeros(1000, 1));
     l_prior(h_loc) =0;
end

% l_prior = log10(h_prior);

h_vals = linspace(h_sd/1001,h_sd,1000)';
log_dh = log(h_vals(6) - h_vals(5));

if strcmp(signal_type, 'Noise')
    [data, true_binary, noise_settings ] = make_all_noise(n_chunks, sigma, h, noise_seed);
    seg_settings = 'NAN';
elseif strcmp(signal_type, 'Signal')
    [data, true_binary, noise_settings] = make_all_signal(n_chunks, sigma, h, noise_seed);
    seg_settings = 'NAN';
elseif strcmp(signal_type, 'Transient')
    [data, true_binary, noise_settings, seg_settings] = make_data(n_chunks, sigma, h, noise_seed, seg_seed);
elseif strcmp(signal_type, 'One segment')
    [data, true_binary, seg_settings, noise_settings] = make_one_segment(n_chunks, sigma, h, seg_seed, noise_seed);
end



bin_list = dec2bin(0:2^(length(data))-1) - '0';
l_likelihood =  zeros(size(bin_list,1),1);  % We would work in log10-space

big_h_vals = repmat(h_vals, size(data));
big_prior = repmat(l_prior, size(data));
big_data = repmat(data, size(h_vals));
P_gamma = zeros(size(bin_list));
l_evidence = zeros(size(bin_list,1),1);

for config = 1:length(bin_list);
    binary_number = (bin_list(config,:)); % The binary configuration that we are considering now
%     binary_number = cat( 2, binary_number, [0,0]);
    
    [block_length, block_numbers, n_breaks, n_changepoints(config) ] = binary_structure( binary_number );
    binary_number = cat(2, binary_number, 0);
    each_h1 = -inf * ones(size(big_h_vals));
    index = 1;
    while index < length(binary_number)
        if binary_number(index) == 1 && binary_number(index+1) ==1

            % Sum the data from the start to the end of the block, also marginalise over h define variable end_of_block to define where coherent marginalisation ends
            end_of_block = index + block_length(block_numbers(index)-1)-1;
            if end_of_block > length(data)
                end_of_block = length(data);
            end
            % each_h1 describes the contribution from each h have that we marginalise over As we have a delta function prior, this should be small for values of h that are not the true value of h. 
            each_h1(:,index:end_of_block) =  -((big_data(:,index:end_of_block) ...
                - big_h_vals(:,index:end_of_block)).^2)/(2*sigma*sigma) + ...
                big_prior(:,index:end_of_block) + log((1/(sqrt(2*pi)*sigma))) ;
            % P_gamma is the sum of these values, log10(sum(prior * gaussian)) Calculate P_gamma chunk by chunk for each chunk in the block
            for row = 0:end_of_block-index;
                P_gamma(config, index+row) = logaddexpvect(each_h1(:,index+row)); %  sum using logaddexpvect for each bit
            end
            index = end_of_block; % Progess the index to end of block
            
        elseif binary_number(index) == 1 && binary_number(index+1) ==0;
            each_h1(:,index) = big_prior(:, index) + log(1/(sqrt(2*pi)*sigma)) - (((big_data(:,index) - big_h_vals(:,index)).^2)/(2*sigma*sigma));
            P_gamma(config,index) = logaddexpvect(each_h1(:,index));
        elseif binary_number(index) == 0
            P_gamma(config,index) =   log(1/(sqrt(2*pi)*sigma)) + (-((data(index)).^2)/(2*sigma*sigma));
        end
        index = index + 1;
        
        l_likelihood(config) = sum(P_gamma(config,:));
        
    end
    if strcmp(CP_prior, 'Flat');
    l_norm(config) = log((1/(length(binary_number)-1))*(nchoosek(length(data)-1,n_changepoints(config))));
    elseif strcmp(CP_prior, 'exp');
         l_norm(config) = log((1/(length(binary_number)-1))*(nchoosek(length(data)-1,n_changepoints(config)))) - n_changepoints;
    else
         l_norm(config) = log((1/(length(binary_number)-1))*(nchoosek(length(data)-1,n_changepoints(config))));
    end
         
    if strcmp(mode, 'prior_only');
         l_evidence(config) = - l_norm(config);
    elseif strcmp(mode, 'normal')
         l_evidence(config) = l_likelihood(config) - l_norm(config);
    elseif strcmp(mode, 'likelihood_only')
         l_evidence(config) = l_likelihood(config);
    end
%     [ l_evidence(config), P_gamma(config) ] = index_loop(binary_number,big_h_vals, big_prior, big_data, P_gamma, l_evidence, data , sigma, n_changepoints(config) , block_length   )
end

l_odds = l_evidence - l_evidence(1);
[sorted_evidence, evidence_index] = sort(exp(l_evidence));
sorted_n_CP = n_changepoints(evidence_index);

% Define the odds of one config vs all other configs
% Denominator is sum of all that are not that index
odds_all = zeros(size(l_evidence));
for index =1:length(l_evidence)
    odds_all_num  = exp(l_evidence(index));
    if index == 1;
        odds_all_denom = sum(exp(l_evidence(index+1:end)));
    elseif index == length(l_evidence);
        odds_all_denom = sum(exp(l_evidence(1:index-1)));
    else
        odds_all_denom_1 = sum(exp(l_evidence(1:index-1)));
        odds_all_denom_2 = sum(exp(l_evidence(index+1:end)));
        odds_all_denom = odds_all_denom_1 + odds_all_denom_2;
    end
    odds_all(index) = odds_all_num/odds_all_denom;
end
[sorted_odds_all, odds_index] = sort(odds_all);
%This doesn't go anywhere yet, but keeping it in here for later.

[sorted_odds, sort_index] = sort(exp(l_odds));
sorted_binaries = bin_list(flipud(sort_index),:);

sorted_priors = l_norm(sort_index);

sanity_check = odds_index - sort_index;

figure
plot(log10(sorted_odds))
title('Sorted odds of a configuration vs Gaussian noise')

figure
plot(log10(sorted_odds_all))
title('Sorted odds of a configuration vs all other configurations')

[  scale, scaled_binaries] = plot_barcode( 16,  flipud(log10(sorted_odds_all)) , sorted_binaries);


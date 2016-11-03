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

clear all
h_sd = 1*10^(-24);
h = rand * h_sd;
sigma = h * 0.001;
hs = linspace(0, h_sd, 1001)
[offset, h_loc] = min(abs(hs - h));

l_prior = log(zeros(1000, 1));
l_prior(h_loc) =0;

h_vals = linspace(h_sd/1001,h_sd,1000)';
[data, true_binary] = make_all_signal(8, sigma, h);

bin_list = dec2bin(0:2^(length(data))-1) - '0';
l_likelihood =  zeros(size(bin_list,1),1);  % We would work in log-space
is_signal = true_binary;
l_odds = zeros(1, length(bin_list));


for config = 1:length(bin_list);
    binary_number = (bin_list(config,:)); % The binary configuration that we are considering now
    binary_number = cat( 2, binary_number, [0,0]);
    
    [block_length, block_numbers, n_breaks, n_changepoints ] = binary_structure( binary_number );
    
    % extend the 'data', l_prior and h_vals variables to all be the same
    big_h_vals = repmat(h_vals, size(data));
    big_prior = repmat(l_prior, size(data));
    big_data = repmat(data, size(h_vals));
    
    each_h1 = -inf * ones(size(big_h_vals));
    index = 1;
    %   P_gamma = log(1);
    while index < length(data) + 1
        if binary_number(index) == 1 && binary_number(index+1) ==0
            each_h1 = big_prior(:, index) + log(1/(sqrt(2*pi)*sigma)) - (((big_data(:,index) - big_h_vals(:,index)).^2)/(2*sigma*sigma));
            P_gamma(config,index) = logaddexpvect(each_h1);
        else
            P_gamma(config,index) =  log(1/(sqrt(2*pi)*sigma)) + (-((data(index)).^2)/(2*sigma*sigma));
        end
        index = index + 1;
        l_likelihood(config) = l_likelihood(config) + sum(P_gamma(config,:));
        
    end
    l_norm = log(nchoosek(length(data)-1,n_changepoints)*(2^(length(data))-1));
    l_evidence(config) = l_likelihood(config) - l_norm;
    l_odds(config) = l_evidence(config) - l_evidence(1);
    
end

figure
plot((l_odds))

% Define the odds of one config vs all other configs
% Denominator is sum of all that are not that index
l_odds_all = zeros(size(l_evidence));
for index =1:length(l_evidence)
    l_odds_all_num = l_evidence(index);
    if index == 1;
        l_odds_all_denom = logaddexpvect(l_evidence(index+1:end));
    elseif index == length(l_evidence);
        l_odds_all_denom = logaddexpvect(l_evidence(1:index-1));
    else
        l_odds_all_denom_1 = logaddexpvect(l_evidence(1:index-1));
        l_odds_all_denom_2 = logaddexpvect(l_evidence(index+1:end));
        l_odds_all_denom = logaddexp(l_odds_all_denom_1, l_odds_all_denom_2);
    end
    l_odds_all(index) = l_odds_all_num/l_odds_all_denom;
end
sorted_odds_all = sort(l_odds_all);
%This doesn't go anywhere yet, but keeping it in here for later.

[sorted_odds, sort_index] = sort(l_odds);
sorted_binaries = bin_list(sort_index,:);
sorted_odds_matrix = transpose(repmat(sorted_odds, 8, 1));

is_max_odds = sorted_binaries(sorted_odds==sorted_odds(end),:);
candidate = sorted_binaries(end,:);

figure
plot(sorted_odds)

scale = ones(size(sorted_odds)).*(-sorted_odds(1) + sorted_odds)./(-sorted_odds(1) + sorted_odds(end));

scaled_binaries = (sorted_binaries-0.5)*2;

for configuration = 1:length(sorted_odds)
    scaled_binaries(configuration,:) = scaled_binaries(configuration,:)*scale(configuration);
end
scaled_binaries = ((scaled_binaries/2) + 0.5);

true_binary;

figure
im = imagesc(scaled_binaries(end-75:end,:));
% alpha(im, (repmat(sorted_odds_matrix(end-50:end,:)/max(sorted_odds_matrix),1, 8)))
colormap(gray)
set(gca,'XGrid','off')
set(gca,'YGrid','on')
colorbar

title('Colour plot of bits sorted by odds radio')
xlabel('Bit position')
ylabel('Position (higher number is more likely)')
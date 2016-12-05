function [ l_evidence, P_gamma ] = index_loop(binary_number,big_h_vals, big_prior, big_data, P_gamma, l_evidence, data , sigma, n_changepoints(config) , block_length )
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here

index = 1;
while index < length(data)
    if binary_number(index) == 1 && binary_number(index+1) ==1
        
        % Sum the data from the start to the end of the block, also marginalise over h define variable end_of_block to define where coherent marginalisation ends
        end_of_block = index + block_length(block_numbers(index)-1)-1;
        if end_of_block > length(data)
            end_of_block = length(data);
        end
        % each_h1 describes the contribution from each h have that we marginalise over As we have a delta function prior, this should be small for values of h that are not the true value of h.
        each_h1(:,index:end_of_block) =  (-(((big_data(:,index:end_of_block) ...
            - big_h_vals(:,index:end_of_block)).^2)/(2*sigma*sigma)));
        % P_gamma is the sum of these values, log10(sum(prior * gaussian)) Calculate P_gamma chunk by chunk for each chunk in the block
        each_h1(:,index) = each_h1(:, index) + log_dh + big_prior(:,index) + log((1/(sqrt(2*pi)*sigma))^(index-end_of_block)) ;
        P_gamma( index) = logaddexpvect(each_h1(:, index)); %  sum using logaddexpvect for each bit
        
        index = end_of_block; % Progess the index to end of block
        
    elseif binary_number(index) == 1 && binary_number(index+1) ==0
        each_h1(:,index) = big_prior(:, index) + log_dh + log(1/(sqrt(2*pi)*sigma)) - (((big_data(:,index) - big_h_vals(:,index)).^2)/(2*sigma*sigma));
        P_gamma(index) = logaddexpvect(each_h1(:,index));
    elseif binary_number(index) == 0
        P_gamma(index) =  log(1/(sqrt(2*pi)*sigma)) + (-((data(index)).^2)/(2*sigma*sigma));
    end
    
%     if index == length(binary_number)
%         if binary_number(index) ==0
%             P_gamma(index) =  log(1/(sqrt(2*pi)*sigma)) + (-((data(index)).^2)/(2*sigma*sigma)) ;
%         elseif binary_number(index) == 1 && binary_number(index-1) == 1
%             P_gamma( index) = 0;
%         elseif binary_number(index) == 1 && binary_number(index-1) == 0
%             each_h1(:,index) = big_prior(:, index) + log_dh + log(1/(sqrt(2*pi)*sigma)) - (((big_data(:,index) - big_h_vals(:,index)).^2)/(2*sigma*sigma));
%             P_gamma(index) = logaddexpvect(each_h1(:,index));
%         end
    end
    index = index + 1;
    l_likelihood = sum(P_gamma(:));
    
end
l_norm = log((1/(length(binary_number)-1))*(nchoosek(length(data)-1,n_changepoints)));%*(2^(length(data))-1));

if strcmp(mode, 'prior_only');
    l_evidence = - l_norm;
else
    l_evidence = l_likelihood - l_norm;
end



end


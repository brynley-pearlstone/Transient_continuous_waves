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

% Call function to break up data into 8 equal length segments

% Call script to run CW code on each of the 8 segments
clear all
h_sd = 1*10^(-24);
h = rand * h_sd
sigma = h * 0.1;
l_prior = log(1/h_sd);
h_vals = h; %linspace(0,h_sd,100)';
[data, true_binary] = make_all_signal(8, sigma, h);

bin_list = (dec2bin([0:2^(length(data))-1])) - '0';
l_likelihood =  zeros(size(bin_list,1),1);  % We would work in log-space
is_signal = true_binary;


for config = 1:size(bin_list,1);
    binary_number = (bin_list(config,:));
%     oldbit = binary_number(1);
    is_breaks = zeros(size(binary_number));
    l_likelihood(config) = log(1/(sqrt(2*pi)*sigma))^(length(data));
    changepoints = 0;

    oldbits = circshift(binary_number,[0,1]);
    oldbits(1) = binary_number(1);
    oldbits(end) = 0; %These lines determine whether any given bit is at the end of a chunk i e a break
    
    is_breaks = circshift(oldbits - binary_number, [0,-1]);
    n_breaks = sum(is_breaks); % If there is a break, we add in the normalisation for the marginalisation over h
   
    l_likelihood(config) = l_likelihood(config) + ( n_breaks * l_prior);
    
    block_start = (binary_number - oldbits==1);
       
    is_changepoint = (oldbits ~= binary_number); %whenever 2 consectutive bits aree not the same, we name it as a changepoint.
    is_changepoint(end) = 0;
    
    n_changepoints = sum(is_changepoint);
    block_number = ones(size(data, 1), size(data, 2)+1);
    n_blocks = sum(block_start);
    block_length = zeros(1,n_blocks);
    block = 1;
    itt = 1;
    for block = 1:block_number(end)
        block_length = 0;
        while binary_number(itt) == 1
            block_length = block_lenth + 1;
            itt = itt + 1;
        end
    end
    
    for itt = 1:length(data) 
        if block_start(itt) ==1
            for count = 0:(length(data) - itt)
                if is_breaks(itt + count) == 1
                    block_length(block) = count + 1;
                    block = block + 1;
                end
            end
        end
        block_number(itt+1) = block_number(itt) +  block_start(itt);
    end
    
    if length(block_length) == 0
        block_length = 0
    end
        
  % extend the 'data' variable to  be the same height as the h_vals variable
  big_h_vals = repmat(h_vals, size(data));
  big_data = repmat(data, size(h_vals));
%   big_h_vals = repmat(h_vals, size(data));
  each_h1 = zeros(size(big_h_vals));
  index = 1;
  P_gamma = log(5);
  while index < length(data) + 1
      if binary_number(index) ==1
          binary_number
          index
          % Sum the data from the start to the end of the block, also
          % marginalise over h
          each_h1(:,index:index + block_length(block_number(itt+1)-1)) = (-((big_data(:,index:index + block_length(block_number(itt+1)-1)) ...
              - big_h_vals(:,index:index + block_length(block_number(itt+1)-1))).^2)/(2*sigma*sigma));
          for row = 1:block_length(block_number(itt+1)-1)
              P_gamma(index + row - 1) = logaddexpvect(each_h1(:, row)) %  sum using logaddexpvect for each bit
          end
          index = index + block_length(block_number(itt+1)-1); % Progess the index to look at next to the end of the block
      else
          P_gamma(index) = (-((data(index)).^2)/(2*sigma^2));
      end
      index = index + 1;
      
      l_likelihood(config) = l_likelihood(config) + sum(P_gamma);
  end
  
%     
%     oldbit = binary_number(1);
%     breaks = 0;
%     for segment = 1:length(data)
%         D = data(segment);
%         bit = (binary_number(segment));
%         
%         if oldbit == 1
%             if bit == 0
%                 breaks = breaks + 1
%                 l_likelihood(config) = l_likelihood(config) + l_prior;
%             end
%         end
%         if oldbit ~= bit
%             changepoints = changepoints + 1;
%         end
%         if bit == 1
%             each_h_1 = (-((D-h_vals).^2)/(2*sigma*sigma));
%             P_gamma = each_h_1; %logaddexpvect(each_h_1);
%             bit1 = 1;
%         end
%         if bit == 0
%             P_gamma = (-((D).^2)/(2*sigma^2));
%             bit0 = 0;
%         end

        l_likelihood(config) = l_likelihood(config) + P_gamma;
        oldbit = bit;
        
    end
	l_norm = log(nchoosek(length(data)-1,changepoints)*(2^(length(data))-1));
    l_likelihood(config) = l_likelihood(config) - l_norm;
    l_odds(config) = l_likelihood(config) - l_likelihood(1);

end

figure
plot((l_odds))
% to_sort = cat(1, l_odds, bin_list');
[number, value] = max(l_odds);
candidate = dec2bin(value, length(data));



[sorted_odds, sort_index] = sort(l_odds);
sorted_binaries = bin_list(sort_index,:);
sorted_odds_matrix = transpose(repmat(sorted_odds, 8, 1));


is_max_odds = sorted_binaries(sorted_odds==sorted_odds(end),:);
candidate = sorted_binaries(end,:);

figure
plot(sorted_odds)

scale = ones(size(sorted_odds)).*sorted_odds./sorted_odds(end);

scaled_binaries = (sorted_binaries-0.5)*2;

for configuration = 1:length(sorted_odds)
    scaled_binaries(configuration,:) = scaled_binaries(configuration,:)*scale(configuration);
end
scaled_binaries = ((scaled_binaries/2) + 0.5);


true_binary;

figure        
im = imagesc(scaled_binaries);
% alpha(im, (repmat(sorted_odds_matrix(end-50:end,:)/max(sorted_odds_matrix),1, 8)))
colormap(gray)
colorbar

title('Colour plot of bits sorted by odds radio')
xlabel('Bit position')
ylabel('Position (1 = most likely)')
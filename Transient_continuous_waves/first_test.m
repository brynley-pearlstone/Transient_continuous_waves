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
sigma = 0.2*10^(-26);
h_sd = 1.5*10^(-24);
bin_list = (dec2bin([0:255]));
prior = 1/h_sd;
[data, true_binary] = make_data(8, sigma);
likelihood = zeros(size(bin_list,1),1);
is_signal = true_binary;

for config = 1:size(bin_list,1);
    binary_number = (bin_list(config,:))
    P_gamma = 1;
    breaks = 0;
    oldbit = binary_number(1);
    prob = 1;
    changepoints = 0;
    for segment = 1:8
        D = data(segment);
        bit = (binary_number(segment));
        if oldbit - bit == 1
            breaks = breaks + 1;
            prob = prob * prior;
        end
        if oldbit - bit ~= 0
            changepoints = changepoints + 1;
        end
        if bit == 1
            P_gamma = (sigma^2*erf((hsd)/sigma*sqrt(2))/(h_sd*D))*exp(-(D^2)/(2*sigma^2))*(exp(h_sd)-1);
            bit1 = 1;
        end
        if bit == 0
            P_gamma = (h_sd/(2*sigma^2))*(exp(-(D^2)/(2*sigma^2)));
            bit0 = 0;
        end

        prob = prob * P_gamma;
        oldbit = bit;
        
    end
	norm = nchoosek(length(data)-1,breaks)*255;
    likelihood(config) = prob / norm;
    odds(config) = likelihood(config)/likelihood(1);
    breaks
    changepoints
end
odds
figure
plot(log10(odds))

%
% 
% end

        

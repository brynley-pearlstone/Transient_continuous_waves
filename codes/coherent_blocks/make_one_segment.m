function [ data, is_signal, seg_settings, noise_settings ] = make_one_segment( n_segs, sigma, h_sd , seg_seed, noise_seed)
% [ segments ] = make_data( n_segs, sigma )
%UNTITLED2 Summary of this function goes here
%   Creates 8 segments of data based on on-off data with aximum CW
%   amplitude in any segment of up to 10^-25.
seg_number = 1:n_segs;
data = zeros(size(seg_number));

if exist('noise_seed')
    rng(noise_seed);
    noise_settings = rng;
    noise = normrnd(0, sigma, size(data));
else
    noise_settings = rng;
    noise = normrnd(0, sigma, size(data));
end

if exist('seg_seed')
    rng(seg_seed);
    seg_settings = rng;
    on_segment= floor((rand*(n_segs-1))+1);
else
    seg_settings = rng;
    on_segment = floor((rand*(n_segs-1))+1);
end

is_signal = zeros(n_segs, 1);
is_signal(on_segment) = 1;
 

h_val = ones(size(data));

aitches = h_sd;

signal_size = aitches * h_val; % + aitch_noise;
for seg = 1:length(data)
    data(seg) = (is_signal(seg) * signal_size(h_val(seg)) + noise(seg));
    data(seg) = abs(data(seg));
end

save('../Data_files/test2.txt', 'data', 'h_sd', '-ascii');

figure
plot(data)
hold on
plot(signal_size, '--')

end


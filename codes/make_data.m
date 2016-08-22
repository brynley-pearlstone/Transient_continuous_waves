function [ data, is_signal ] = make_data( n_segs, sigma )
% [ segments ] = make_data( n_segs, sigma )
%UNTITLED2 Summary of this function goes here
%   Creates 8 segments of data based on on-off data with aximum CW
%   amplitude in any segment of up to 10^-25.
seg_number = 1:n_segs;
data = zeros(size(seg_number));

noise = normrnd(0, sigma, size(data));

for seg = 1:8
    if rand > 0.5
        is_signal(seg) = 1;
    else
        is_signal(seg) = 0;
    end
end
is_signal

signal = is_signal
h_val = ones(size(data));

for position = 2:length(signal)
    oldbit = signal(position-1);
    bit = signal(position);
    if oldbit - bit ==-1
        h_val(position:end) = h_val(position) + 1;
    end
end

h_val

aitches = rand(size(data))*10^(-25);
aitch_noise = rand(size(data))*10^(-26);

signal_size = aitches + aitch_noise;
for seg = 1:length(data)
    data(seg) = (is_signal(seg) * signal_size(seg)) + noise(seg);
    data(seg) = abs(data(seg));
end





end


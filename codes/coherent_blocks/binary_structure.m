function [block_length, block_numbers, n_breaks,n_changepoints ] = binary_structure( binary_number )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

oldbits = circshift(binary_number, [0,1]);
block_end = circshift((oldbits - binary_number==1), [0,-1]); % Compare where thhe number is not to where it used to be to determine if a block has ended
n_breaks = sum(block_end); % If there is a break, we add in the normalisation for the marginalisation over h


block_start = (binary_number - oldbits==1);

is_changepoint = (oldbits ~= binary_number); % whenever 2 consectutive bits aree not the same, we name it as a changepoint.
n_changepoints = sum(is_changepoint);
if n_changepoints>length(binary_number)-3
    n_changepoints=length(binary_number)-3;
end

block_number = ones(size(binary_number, 1), size(binary_number, 2));
n_blocks = sum(block_start);
block_length = zeros(1,n_blocks);
block = 1;
itt = 1;

while itt < length(binary_number)
    if block_start(itt) ==1
        count = 0;
        while block_end(itt+count) ==0
            count = count + 1;
        end
        block_length(block) = count + 1;
        block = block + 1;
    end
    block_number(itt+1) = block_number(itt) +  block_start(itt);
    itt = itt+1;
end
block_numbers = block_number(2:end);
if isempty(block_length)
    block_length = 0;
end
end


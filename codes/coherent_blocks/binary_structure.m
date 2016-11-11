function [block_length, block_numbers, n_breaks,n_changepoints ] = binary_structure( binary_number )
% This function deconstructs the binary number and determined how many
% blocks, how many changepoints, and where each block begins and ends.

clipped_binary = binary_number; %(1:end-2);
is_changepoint = abs(diff(clipped_binary));
n_changepoints = sum(is_changepoint);

bookend_binary = cat(2, 0,clipped_binary, 0);

block_end = (diff(bookend_binary)<0); % Compare where thhe number is not to where it used to be to determine if a block has ended
n_breaks = sum(block_end); % If there is a break, we add in the normalisation for the marginalisation over h

block_start = (diff(bookend_binary)>0);

block_number = ones(size(binary_number));
n_blocks = sum(block_start);

block_length = zeros(1,n_blocks);
block = 1;
itt = 1;

for itt = 1:length(binary_number)-1;
    if block_start(itt) ==1
        count = 0;
        while block_end(itt+count) ==0;
            count = count + 1;
        end
        block_length(block) = count; 
        block = block + 1;
    end
    block_number(itt+1) = block_number(itt) +  block_start(itt);
end

block_numbers = block_number(2:end);
if isempty(block_length)
    block_length = 0;
end
end


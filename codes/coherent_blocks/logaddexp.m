function [ z ] = logaddexp( x, y )
%UNTITLED Summary of this function goes here
%   Input 2 log values to be summed. Output double precision
%   output which is the sum of the inputs.

z = log(exp(x - y) + 1) + y;
end




function [ y ] = logaddexpvect( x )

%UNTITLED Summary of this function goes here
%   Input 2 log values to be summed. Output double precision
%   output which is the sum of the inputs.

running_answer = -inf;
for itteration = 1:length(x)
   running_answer = logplus(running_answer, x(itteration));
end
y = running_answer;
end
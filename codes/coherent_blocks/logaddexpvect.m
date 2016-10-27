function [ y ] = logaddexpvect( x )

%UNTITLED Summary of this function goes here
%   Input 2 log values to be summed. Output double precision
%   output which is the sum of the inputs.

running_answer = x(1);
if length(x)>1;
    for itteration = 2:length(x)
        new_answer = log(exp(x(itteration) - running_answer) + 1) + running_answer;
        running_answer = new_answer;
    end
end
y = running_answer;

end








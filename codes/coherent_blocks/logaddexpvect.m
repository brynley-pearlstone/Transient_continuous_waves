function [ y ] = logaddexpvect( x )

%UNTITLED Summary of this function goes here
%   Input 2 log values to be summed. Output double precision
%   output which is the sum of the inputs.

% e_vect = exp(x);
% sum_vect = sum(e_vect);
% y = log(sum_vect);
% This is the by-the numbers way to do it. This often results in inf and
% -inf outputs

% running_answer = x(1);
% if length(x)>1;
%     for itteration = 2:length(x)
%         new_answer = log(exp(x(itteration) - running_answer) + 1) + running_answer;
%         running_answer = new_answer;
%     end
% end
% y = running_answer;
% This is my first try at a fix following the standard method. This still
% sometimes results in +/-inf values for high SNR

running_answer = x(1);
if length(x)>1
    for itteration = 2:length(x)
        new_answer = max(running_answer, x(itteration)) + log(exp(running_answer - max(running_answer, x(itteration)) ) + exp(x(itteration) - max(running_answer, x(itteration)) ));
        running_answer = new_answer;
    end
end
y = running_answer;
% This third attempt is an approximation which should prevent overflow and
% underflow, but still result in some infinities.

end
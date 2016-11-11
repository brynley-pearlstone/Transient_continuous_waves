% Sanity script should call the function to output checks against some
% clear sanity checks

% Call coherent_RBB with all signal at SNR ~1000, delta function prior
% Check that output is all signal with log odds difference ~10^6 between
% first 2 results
 [ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(8, 'Signal', 'delta', 1000 , 'not prior_only');
check_1 = sorted_odds(end) - sorted_odds(end-1)
if check_1/1000000 < 0.1;
    error('Error! \nThere is something wrong with the way likelihoods are being handled - not significant enough!')
end

% Call coherent_RBB with all noise
% Check that all noise result is favoured
 [ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(8, 'Noise', 'delta', 100 , 'not_prior_only');
if sorted_binaries(end) ~= [0,0,0,0,0,0,0,0]
    error('Error! \nMost likely configuration for all noise input contains signal!')
end
% Call coherent_RBB with only the prior on N_cp left in
% Check that this corresponds with what we wanted
[ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(8, 'Signal', 'delta', 100 , 'prior_only');



%Call coherent RBB with only 2 chunks, see if other tests still hold
[ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(2, 'Signal', 'delta', 1000 , 'not_prior_only');
check_1 = sorted_odds(end) - sorted_odds(end-1)
if check_1/1000000 < 0.1;
    error('Error! \nThere is something wrong with the way likelihoods are being handled - not significant enough!')
end

[ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(2, 'Noise', 'delta', 100 , 'not_prior_only');
if sorted_binaries(end) ~= [0,0]
    error('Error! \nMost likely configuration for all noise input contains signal!')
end
% Call coherent_RBB with only the prior on N_cp left in
% Check that this corresponds with what we wanted
[ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(2, 'Signal', 'delta', 100 , 'prior_only');

[ sorted_binaries, sorted_odds, sorted_n_CP ] = RBB_func(2, 'Signal', 'delta', 100 , 'prior_only');

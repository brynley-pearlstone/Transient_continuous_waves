function [ scale, scaled_binaries] = plot_barcode( to_plot, sorted_odds , sorted_binaries)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

% to_plot = length(sorted_odds) - ;

% Define the scaling factor for the barcode plot. 
% odds should come in sorted already. With the highest number at the end.
% (NOTE: NEGATIVE NU|M|BERS)
% Lowest in the range = 0, largest in the range = 1.

scale_max = sorted_odds(end) - sorted_odds(to_plot);
scale = sorted_odds(to_plot:end) - sorted_odds(to_plot);
scale = scale /scale_max;
% Now, to scale, we must have something to scale. The binaries go from 0 to
% 1, so they can't be multiplicatively scaled. We subtract 0.5 from each
% binary number, so that they can be scaled correctly. Then we multiply by
% 2, so that they run from -1 to +1.
% Then we can multiply by scale, so that the binarys run from +/- 0 to
% +/-1. 
% Then we add 1, and divide by 2, so they run from 0.5+/- delta to 0/1

% scaled_binaries = (sorted_binaries(to_plot:end,:)-0.5)*2;

scaled_binaries = (sorted_binaries(to_plot:end,:));

for configuration = 1:length(scale)
    scaled_binaries(configuration,:) = scaled_binaries(configuration,:)*scale(configuration);
end

% scaled_binaries = (scaled_binaries + 1)/2;


scaled_binaries = (scaled_binaries );

figure
im = imagesc(scaled_binaries(1:end,:));
% alpha(im, (repmat(sorted_odds_matrix(end-50:end,:)/max(sorted_odds_matrix),1, 8)))
colormap(gray)
colormap(flipud(colormap))
set(gca,'XGrid','off')
set(gca,'YGrid','on')
colorbar

title('Colour plot of bits sorted by odds radio')
xlabel('Bit position')
ylabel('Position (higher number is more likely)')

end


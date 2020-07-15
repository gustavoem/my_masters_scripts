%
% Correct-model: A Ras small GTPase molecular switch dynamic model.
%
%                  This model must be used for the generation of
%                  timeseries for the model selection procedure.
%

% Copyright (C) 2020  Marcelo S. Reis and Gustavo Estrela.
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.


% Model definition.
%
function dy = CorrectModel (y, t)
 
  dy = zeros (8,1);
  
  k1    = 1.8e-4;
  d1    = 3.0;
  k2    = 1.7e-4;
  d2    = 0.04;
  k3cat = 3.8;      % k3cat is x100 larger than the original one
  K3m   = 1.64e3;   % to yield an early Ras activation.
  k4cat = 0.003;
  K4m   = 9.12e3;
  k5cat = 0.1;
  K5m   = 1.07e2;
  k6cat = 0.01;
  K6m   = 1836;
  
  % d[SOS]/dt
  %
  dy(1) = - (k1 * y(1) * y(4)) + (d1 * y(2)) - (k2 * y(1) * y(5)) + (d2*y(3));
  
  % d[SOS_allo_RasGDP]/dt
  %
  dy(2) = + (k1 * y(1) * y(4)) - (d1 * y(2));

  % d[SOS_allo_RasGTP]/dt
  %
  dy(3) = + (k2 * y(1) * y(5)) - (d2 * y(3));

  % d[RasGDP]/dt
  %
  dy(4) = - (k1 * y(1) * y(4)) + (d1 * y(2)) ... 
          - (k3cat * y(3) * y(4))/(K3m + y(4)) ...
          - (k4cat * y(2) * y(4))/(K4m + y(4)) ...
          + (k5cat * y(7) * y(5))/(K5m + y(5)) ...
          - (k6cat * y(6) * y(4))/(K6m + y(4));

  % d[RasGTP]/dt
  %
  dy(5) = + (d2 * y(3)) - (k2 * y(1) * y(5)) ...
          + (k3cat * y(3) * y(4))/(K3m + y(4)) ...
          + (k4cat * y(2) * y(4))/(K4m + y(4)) ...
          - (k5cat * y(7) * y(5))/(K5m + y(5)) ...
          + (k6cat * y(6) * y(4))/(K6m + y(4));

  % d[GEF]/dt
  %
  dy(6) = 0;

  % d[GAP]/dt
  %
  dy(7) = 0;  
  
  % d[iGAP]/dt
  %
  dy(8) = 0;

endfunction


% Numeric integration of the model.
%
interval = linspace (0, 200, 201);  % 200 units divided in 201 points.


% Simulate with SOS (y(1)) = 10 (G0) and also = 200 (after stimulation).
%
[T, istate, msg] = lsode ("CorrectModel", ...
                          [200; 0; 0; 900; 100; 200; 125; 275],...
                          interval);


% Plotting the results.
%
clf;
plot(interval,T(:,2), "linewidth", 4, interval,T(:,3), "linewidth", 4, ...
     interval,T(:,4), "linewidth", 4, interval,T(:,5), "linewidth", 4);
legend("SOS_{allo}^{RasGDP}", "SOS_{allo}^{RasGTP}", "RasGDP", "RasGTP", ...
       "Location","NorthEastOutside");
set(gca, "linewidth", 4, "fontsize", 12)
xlabel("time (AU)"); ylabel("concentration (AU)");


% End of program.
%

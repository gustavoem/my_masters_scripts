%
% Empty-model: A Ras small GTPase molecular switch dynamic model.
%
%                  This model has no reaction at all.
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
function dy = EmptyModel (y, t)
 
  dy = zeros (8,1);
    
  % d[SOS]/dt
  %
  dy(1) = 0;
  
  % d[SOS_allo_RasGDP]/dt
  %
  dy(2) = 0;

  % d[SOS_allo_RasGTP]/dt
  %
  dy(3) = 0;

  % d[RasGDP]/dt
  %
  dy(4) = 0;

  % d[RasGTP]/dt
  %
  dy(5) = 0;

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
[T, istate, msg] = lsode ("EmptyModel", ...
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


function [Filtered_Motion,Time]=Fourier_Amplitude(x,dt,fmin,fmax)

%Filtered Signal Frequency (SFBMD)
%--------------------------------------------------------------------------
% This function filters the signal within a particular frequency f_min and f_max
% and outputs the filtered signal and time.
%
% SYNTAX
%       Fourier_Amplitude(x,dt,fmin,fmax)
%
% INPUT
%       [x] :      	    signal data [nx1]
%       [dt]:    		time step [1x1]
%       [fmin]:    		minimum frequency [1x1]
%       [fmax]:    		minimum frequency [1x1]
%
% OUTPUT
%       Filtered_Motion:      Filtered Signal [nx1]
%       Time:     	          Time [nx1]
%       Plot:     	          Original and Filtered Signal
%
%
% EXAMPLE
%   - for a square pulse 
%	tm   = [[0:0.0001:0.5],[0.5+0.0001:0.0001:0.7],[0.7+0.0001:0.0001:2]];
%	acc  = [linspace(0,0,(0.5/0.0001)),linspace(0.5,0.5,(0.2/0.0001)+1),linspace(0,0,(1.3/0.0001))];
%   ky = 0.2;
%   NewmarkSb (tm,acc,ky);
%
%==========================================================================
%                     2017 By: Sumeet Kumar Sinha (sumeet.kumar507@gmail.com)


	%This function calculates the FFT of the function 

	X = x(:,1);
	dT = dt;        % Time Period 
	F_s = 1/dT;     % Sampling Frequency
	L = size(X,1);  % Length of the Signal
	T = (dt:dt:L*dt)'; 

	New_L =L;
	New_X=X;
	New_T=T;

	Y = fft(New_X);
	Index_Middle = (New_L+1)/2;

	Amp  = abs(Y);
	Phase_Angle = atan(real(Y)./imag(Y));

	Pos_Amp  = Amp(1:Index_Middle);
	Pos_Phase_Angle = Phase_Angle(1:Index_Middle);
	Pos_Freq = ((0:F_s:F_s*(New_L-1)/2)/New_L)';


	%%%%%%%% Filtering Frequency %%%%%%%%%

	Index_Start  = 1+round(fmin*New_L/F_s);
	Index_End    = 1+round(fmax*New_L/F_s);

	if(Index_End>((New_L+1)/2))
		Index_End = ((New_L+1)/2);
	end

	if(Index_Start~=1)
		Pos_Amp(1:Index_Start)= 0;
		Y(1:Index_Start)=0;
		Y(end-Index_Start:end)=0;
	end

	Pos_Amp(Index_End:Index_Middle)=0;
	Y(Index_End:Index_Middle)=0;
	Y(Index_Middle:2*Index_Middle-Index_End)=0;

	%%%%%%%%% Inverse FFT %%%%%%%%%%%%%%

	figure ;
	IFFT_X = ifft(Y);
	plot(New_T,IFFT_X);
	hold on;
	plot(New_T,New_X);
	title('Signal ');
	xlabel('Time [s]');
	ylabel('X(T)');

	Filtered_Motion = IFFT_X;
	Time = New_T;

end
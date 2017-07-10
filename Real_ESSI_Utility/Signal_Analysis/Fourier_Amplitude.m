
function Fourier_Amplitude(x,dt,Signal_Name)

	%This function calculates the FFT of the function 

	X = x(:,1);
	dT = dt;        % Time Period 
	F_s = 1/dT;     % Sampling Frequency
	L = size(X,1);  % Length of the Signal
	T = (dt:dt:L*dt)'; 

	display(dT); 
	display(F_s);
	display(L);

	% New_L = 2^round(log2(L)+0.5)+1;
	% New_X = zeros(New_L,1);
	% New_X(1:L) = X;
	% New_T = zeros(New_L,1);
	% New_T(1:L) = T;
	% New_T(L:New_L) = (New_T(L):dT:New_T(L)+(New_L-L)*dT)';

	New_L =L;
	New_X=X;
	New_T=T;

	% plot(T,X);
	% title(Signal_Name);
	% xlabel('Time [s]');
	% ylabel('X(t)');

	Y = fft(New_X);
	Index_Middle = (New_L+1)/2;

	Amp  = abs(Y);
	Phase_Angle = atan(real(Y)./imag(Y));

	Pos_Amp  = Amp(1:Index_Middle);
	Pos_Phase_Angle = Phase_Angle(1:Index_Middle);
	Pos_Freq = ((0:F_s:F_s*(New_L-1)/2)/New_L)';


	Pos_Amp= Pos_Amp/L;
	Pos_Amp(1)= Pos_Amp(1)/2;

	% figure;
	loglog(Pos_Freq,Pos_Amp,'LineWidth',2);
	title(strcat('Fourier Amplitude of ',Signal_Name) );
	xlabel('f(Hz)');
	ylabel('|Fourier Amplitude|');

end
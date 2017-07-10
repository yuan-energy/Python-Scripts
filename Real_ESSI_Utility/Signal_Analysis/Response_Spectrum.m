clc; clear all; 
load x.txt;
T = x(:,1);
X = x(:,2);
dT = T(2)-T(1); % Time Period 
F_s = 1/dT;     % Sampling Frequency
L = size(T,1);  % Length of the Signal 

display(dT); 
display(F_s);
display(L);

New_L = 2^round(log2(L)+0.5)+1;
New_X = zeros(New_L,1);
New_X(1:L) = X;
New_T = zeros(New_L,1);
New_T(1:L) = T;
New_T(L:New_L) = (New_T(L):dT:New_T(L)+(New_L-L)*dT)';

plot(New_T,New_X);
title('Signal ');
xlabel('Time [s]');
ylabel('X(T)');

Y = fft(New_X);
Index_Middle = (New_L+1)/2;


Amp  = abs(Y);
Phase_Angle = atan(real(Y)./imag(Y));

Pos_Amp  = Amp(1:Index_Middle);
Pos_Phase_Angle = Phase_Angle(1:Index_Middle);
Pos_Freq = ((0:F_s:F_s*(New_L-1)/2)/New_L)';

figure;
loglog(Pos_Freq,Pos_Amp);
title('Amplitude Spectrum of X(t)');
xlabel('f(Hz)');
ylabel('|C_n(f)|');

%%%%%%%% Filtering Frequency %%%%%%%%%
F_start = 0.1;
F_end   = 20;

Index_Start  = 1+round(F_start*New_L/F_s);
Index_End    = 1+round(F_end*New_L/F_s);

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

hold on;
loglog(Pos_Freq,Pos_Amp);
title('Amplitude Spectrum of X(t)');
xlabel('f(Hz)');
ylabel('|C_n(f)|');


%%%%%%%%% Inverse FFT %%%%%%%%%%%%%%

% figure; 
% IFFT_X = ifft(Y);

% loglog(Pos_Freq,Pos_Amp);
% figure;
% semilogx(Pos_Freq,Pos_Phase_Angle);

figure ;
IFFT_X = ifft(Y);
plot(New_T,IFFT_X);
hold on;
plot(New_T,New_X);
title('Signal ');
xlabel('Time [s]');
ylabel('X(T)');








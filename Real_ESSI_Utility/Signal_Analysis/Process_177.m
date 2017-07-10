clc; clear all; 
load Input_177.txt;

dt = 0.029070;
sz = 689;

El_x = Input_177(1,:)';
El_y = Input_177(2,:)';
El_z = Input_177(3,:)';

El_Pl_x = Input_177(10,:)';
El_Pl_y = Input_177(11,:)';
El_Pl_z = Input_177(12,:)';

T = (dt:dt:689*dt)';


Fourier_Amplitude(El_y,dt,' Displcement\_Y');
hold on;
Fourier_Amplitude(El_Pl_y,dt,' Displcement\_Y');

legend('Elastic No Contact','Elast0 Plastic With Contact')

print('Elastic_No_Contact_Elasto_Plastic_With_Contact_FFT_Displacement_Y', '-dpdf'); %<-Save as PNG with 300 DPI


% Fourier_Amplitude(El_Pl_x,dt,' Displcement\_X');
% hold on;
% Fourier_Amplitude(El_x,dt,' Displcement\_X');

% legend('Elastic No Contact','Elasto Plastic With Contact')

% print('Displacement_X', '-dpng', '-r300'); %<-Save as PNG with 300 DPI


% Fourier_Amplitude(El_Pl_y,dt,' Displcement\_Y');
% hold on;
% Fourier_Amplitude(El_y,dt,' Displcement\_Y');

% legend('Elastic No Contact','Elasto Plastic With Contact')

% print('Displacement_Y', '-dpng', '-r300'); %<-Save as PNG with 300 DPI

% T = x(:,1);
% X = x(:,2);
% dT = T(2)-T(1); % Time Period 
% F_s = 1/dT;     % Sampling Frequency
% L = size(T,1);  % Length of the Signal 

% display(dT); 
% display(F_s);
% display(L);

% New_L = 2^round(log2(L)+0.5)+1;
% New_X = zeros(New_L,1);
% New_X(1:L) = X;
% New_T = zeros(New_L,1);
% New_T(1:L) = T;
% New_T(L:New_L) = (New_T(L):dT:New_T(L)+(New_L-L)*dT)';

% plot(New_T,New_X);
% title('Signal ');
% xlabel('Time [s]');
% ylabel('X(T)');

% Y = fft(New_X);
% Index_Middle = (New_L+1)/2;


% Amp  = abs(Y);
% Phase_Angle = atan(real(Y)./imag(Y));

% Pos_Amp  = Amp(1:Index_Middle);
% Pos_Phase_Angle = Phase_Angle(1:Index_Middle);
% Pos_Freq = ((0:F_s:F_s*(New_L-1)/2)/New_L)';

% % figure;
% loglog(Pos_Freq,Pos_Amp);
% title('Amplitude Spectrum of X(t)');
% xlabel('f(Hz)');
% ylabel('|C_n(f)|');

% %%%%%%%% Filtering Frequency %%%%%%%%%
% F_start = 0.1;
% F_end   = 20;

% Index_Start  = 1+round(F_start*New_L/F_s);
% Index_End    = 1+round(F_end*New_L/F_s);

% if(Index_End>((New_L+1)/2))
% 	Index_End = ((New_L+1)/2);
% end

% if(Index_Start~=1)
% 	Pos_Amp(1:Index_Start)= 0;
% 	Y(1:Index_Start)=0;
% 	Y(end-Index_Start:end)=0;
% end

% Pos_Amp(Index_End:Index_Middle)=0;
% Y(Index_End:Index_Middle)=0;
% Y(Index_Middle:2*Index_Middle-Index_End)=0;

% hold on;
% loglog(Pos_Freq,Pos_Amp);
% title('Amplitude Spectrum of X(t)');
% xlabel('f(Hz)');
% ylabel('|C_n(f)|');


% %%%%%%%%% Inverse FFT %%%%%%%%%%%%%%

% % figure; 
% % IFFT_X = ifft(Y);

% % loglog(Pos_Freq,Pos_Amp);
% % figure;
% % semilogx(Pos_Freq,Pos_Phase_Angle);

% figure ;
% IFFT_X = ifft(Y);
% plot(New_T,IFFT_X);
% hold on;
% plot(New_T,New_X);
% title('Signal ');
% xlabel('Time [s]');
% ylabel('X(T)');








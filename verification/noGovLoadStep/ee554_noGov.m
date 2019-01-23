%%  ee554_noGov.m
%   Thad Haines         Research
%   Program Purpose:    Import data from PSLF and LTD .mat
%                       Make plots 
%                       Relies on udread.m and jplot.m
%                       print_f requires altmany export fig
%
%   History:
%   01/19/19    08:32   init
%   01/19/19    12:48   verification of Euler with Frequency effects


%% init
clear; format compact; clc; close all; 

print_f = 0;
p_pos = [400 200 1300 650];
grey = [.7 .7 .7];
bfz = 15;
l_loc = 'best';

%% import pslf data

pslf_data = udread('ee554.exc.2.chf',[]);
cellfun(@disp,pslf_data.Name)

spd_col = jfind(pslf_data, 'spd')
v_col = jfind(pslf_data, 'v')
pg_col = jfind(pslf_data, 'pg')
qg_col = jfind(pslf_data, 'qg')
f_col = jfind(pslf_data, 'fbu')

t = pslf_data.Data(:,1);

%% import LTD data
load('noGov.mat') % euler f integration
load('noGovAB.mat') % adams bashforth integration
load('noGovABHres.mat') % adams bashforth integration, 0.25 timestep
load('noGovABHw.mat') % accounts for freq in swing equation
load('noGovEw.mat') % accounts for freq in swing equation
t_1 = noGov.t;
f_1 = noGov.f;


%% plot pslf Voltage
figure('pos',p_pos)
subplot 223
plot(t,pslf_data.Data(:,v_col(1)),'-','linewidth',4,'color',[.7 .7 .7])
hold on
plot(t,pslf_data.Data(:,v_col(2)),':','linewidth',5,'color','k')

stairs(t_1,noGov.A1.S11.Vm,'-o','linewidth',1.5,'color',[1 0 1])
stairs(t_1,noGov.A1.G21.Vm,':s','linewidth',1,'color',[0 1 1])


title_str = 'Generator Voltage';
y_label = 'Voltage [pu]';

grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','LTD Gen 1','LTD Gen 2'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

if print_f == 1
    set(gcf,'color','w'); % to remove border of figure
    export_fig('XXXXXX','-pdf'); % to print fig
end % end print f

%% plot pslf real power generated
subplot 221
plot(t,pslf_data.Data(:,pg_col(1)),'-','linewidth',4,'color',[.7 .7 .7])
hold on
plot(t,pslf_data.Data(:,pg_col(2)),':','linewidth',5,'color','k')

stairs(t_1,noGov.A1.S11.S0.Pe,'-o','linewidth',1.5,'color',[1 0 1])
stairs(t_1,noGov.A1.G21.G0.Pe,':s','linewidth',1,'color',[0 1 1])

title_str = 'Real Power Generated';
y_label = 'MW';

grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','LTD Gen 1','LTD Gen 2'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot generator frequency
subplot 222
plot(t,pslf_data.Data(:,f_col(1))/60,'-','linewidth',4,'color',[.7 .7 .7])
hold on
plot(t,pslf_data.Data(:,f_col(2))/60,':','linewidth',5,'color','k')

plot(t_1,f_1,'-o','linewidth',1.5,'color',[1,0,1])
plot(noGovAB.t,noGovAB.f,':s','linewidth',1.5,'color',[0,1,1])
plot(noGovEw.t,noGovEw.f,':s','linewidth',1.5,'color',[1,0,0])
plot(noGovABHw.t,noGovABHw.f,':s','linewidth',1.5,'color',[0,0,1])

title_str = 'Generator Frequency';
y_label = 'Frequency [pu]';
grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2', 'LTD Euler','LTD AB','LTD Euler w Freq','LTD AB w Freq'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% plot pslf q power generated
subplot 224
plot(t,pslf_data.Data(:,qg_col(1)),'-','linewidth',4,'color',[.7 .7 .7])
hold on
plot(t,pslf_data.Data(:,qg_col(2)),':','linewidth',5,'color','k')

stairs(t_1,noGov.A1.S11.S0.Q,'o-','linewidth',1.5,'color',[1 0 1])
stairs(t_1,noGov.A1.G21.G0.Q,'s:','linewidth',1,'color',[0 1 1])

title_str = 'Reactive Power Generated';
y_label = 'MVAR';

grid on
set(gca,'FontSize',.85*bfz)
legend({'PSLF Gen 1','PSLF Gen 2','LTD Gen 1','LTD Gen 2'}, ...
    'Fontsize',bfz*.9,'location',l_loc) % Legend
set(gcf,'Position',p_pos)
title(title_str, 'Fontsize',bfz)
ylabel(y_label, 'Fontsize',bfz)
xlabel('Time [sec]', 'Fontsize',bfz)

%% relative frequency
% index of t == 0 in PSLF data
zoft = 3;
ts = t(zoft+1); % first time step from zero
fs = round(1/ts);

f = pslf_data.Data(:,f_col(2))/60; % per unit freq

for ct=0:20
    % find index of time at full second
    n = zoft + fs*ct;
    % pull values
    pulledtime(ct+1) = t(n);
    pulledf(ct+1) = f(n);
    
    ct= ct+1;
end

% calculate relative freq
rFEw = noGovEw.f-pulledf;
rFE = noGov.f - pulledf;
rFAB = noGovAB.f-pulledf;
rFABw = noGovABHw.f -pulledf;

%{
%% make plot
figure
plot(pulledtime,rFE,':o','Linewidth',2)
hold on
plot(pulledtime,rFAB,':o','Linewidth',2)
plot(pulledtime,rFEw,':+','Linewidth',2)
plot(pulledtime,rFABw,':+','Linewidth',2)
grid on
xlim([0,16])
xlabel('Time [sec]')
ylabel('Relative Frequency [pu]')
title('PSLF v LTD Relative Frequency')
legend({'Euler','A.B.','Euler w Freq Fx','A.B. w Freq Fx'},'location','best')
set(gca,'FontSize',15)

%}

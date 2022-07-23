clear all 
close all
clc

N = 1000;         % All points
M = 20;          % Num of those points in least square
max_dist = 5000; % in mm (room scale)
adjust = 0.5;    % Adjust for camera fov
noise_mult = 0.001;   % percentage

% Make random transformation matrix
R = rotx(360*rand(1,1)) * roty(360*rand(1,1)) * rotz(360*rand(1,1));
t = max_dist * rand(3,1) + 2000;
T = [R, t ; 0,0,0,1];

% Least square
% a = [0,0,1,1 ; 0,1,0,1 ; 1,0,0,1 ; 0,0,0,1]';
a = [adjust*max_dist*randn(3,N) ; ones(1,N)];               % Generate N points
b = T*a + [max_dist*noise_mult*randn(3,N) ; zeros(1,N)]; % Transform points and add some noise

bb = reshape(b,[],1);
ab = zeros(N,16);
for j=1:N
    for i=1:4
        ab(4*(j-1)+i,:) = [zeros(1, 4*(i-1)), a(:,j)', zeros(1, 4*(4-i))];
    end
end

% ab*Tt = bb ->
Tt = ab\bb;
Tt = reshape(Tt, 4,4)';
Tt(4,1:3) = [0,0,0]
a_out = inv(Tt)*b;




%% 2nd iteration

% b2 = T*a_out + [N*noise*randn(3,N) ; zeros(1,N)];
% bb2 = reshape(b2,[],1);
% ab2 = zeros(N,16);
% for j=1:N
%     for i=1:4
%         ab(4*(j-1)+i,:) = [zeros(1, 4*(i-1)), a(:,j)', zeros(1, 4*(4-i))];
%     end
% end
% % ab*Tt = bb ->
% Tt2 = ab\bb;
% Tt2 = reshape(Tt2, 4,4)';
% a_out2 = inv(Tt2)*b2;



%% Plot
figure
plot3(a(1,:),a(2,:),a(3,:),'r.',b(1,:),b(2,:),b(3,:),'go'), hold on, axis equal
title("Before least square");

figure
plot3(a(1,:),a(2,:),a(3,:),'r.',a_out(1,:),a_out(2,:),a_out(3,:),'go'), hold on, axis equal
title("After least squares");



% metrics
error = vecnorm(a(1:3,:)-a_out(1:3,:));
mean_error = mean(error) / max_dist

trans_error = vecnorm(T(1:3,4) - Tt(1:3,4))

% R = T(1:3,1:3);
R_out = Tt(1:3,1:3);
v1 = R*[1;0;0];
v2 = R_out*[1;0;0];
ang_error = acos(dot(v1, v2) / (norm(v1) * norm(v2))) * 180 / pi

% error2 = vecnorm(a(1:3,:)-a_out2(1:3,:));
% mean_error2 = mean(error)
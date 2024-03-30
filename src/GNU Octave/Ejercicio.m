clear, clc
pkg load symbolic
syms L1 L2 Q1 Q2 Q3 Q4

l1 = 5;
l2 = 5;
q1 = pi/3;
q2 = pi/2;
q3 = 1;
q4 = 2;

DH10 = DH(q1, l1, 0, pi/2);

%DH21 = HRz(pi/2 + q2) * HTz(0) * HTx(0) * HRx(pi/2)

%DH32 = HRz(pi/2) * HTz(l2+q3) * HTx(0) * HRx(pi/2)

%DH43 = HRz(0) * HTz(q4) * HTx(0) * HRx(0)

DH = DH10 %* DH21 * DH32 * DH43;
%DH

p_final = [0;0;0;1];

point = round(DH * p_final .*100) / 100

function HR = HRx(alpha)
  dato = whos('alpha');

  if strcmp(dato.class, 'sym')
    HR=[
      1 * alpha ^ 0,    0,            0,              0;
      0,                cos(alpha),   -sin(alpha),    0;
      0,                sin(alpha),   cos(alpha),     0;
      0,                0,            0,              1* alpha ^ 0;
      ];

    else
      HR=[
      1,   0,            0,              0;
      0,   cos(alpha),   -sin(alpha),    0;
      0,   sin(alpha),   cos(alpha),     0;
      0,   0,            0,              1;
      ];
  end
end


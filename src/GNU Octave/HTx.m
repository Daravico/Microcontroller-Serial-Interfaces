function T = HTx(B)
  dato = whos('B');

  if strcmp(dato.class, 'sym')
    T=[
      1 * B ^ 0,  0,                0,              B;
      0,             1 * B ^ 0,     0,              0;
      0,             0,                1 * B ^ 0,   0;
      0,             0,                0,           1* B ^ 0;
      ];

    else
      T=[
      1,  0, 0, B;
      0,  1, 0, 0;
      0,  0, 1, 0;
      0,  0, 0, 1;
      ];
  end
end

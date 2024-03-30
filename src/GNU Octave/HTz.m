function T = HTz(a)
  dato = whos('a');

  if strcmp(dato.class, 'sym')
    T=[
      1 * a ^ 0,      0,                0,              0;
      0,              1 * a ^ 0,        0,              0;
      0,              0,                1 * a ^ 0,      a;
      0,              0,                0,              1* a ^ 0;
      ];

    else
      T=[
      1,  0, 0, 0;
      0,  1, 0, 0;
      0,  0, 1, a;
      0,  0, 0, 1;
      ];
  end
end

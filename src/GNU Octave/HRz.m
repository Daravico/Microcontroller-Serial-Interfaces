function HR = HRz(theta)
  dato = whos('theta');

  if strcmp(dato.class, 'sym')
    HR=[
      cos(theta),   -sin(theta),  0,              0;
      sin(theta),   cos(theta),   0,              0;
      0,            0,            1 * theta ^ 0,  0;
      0,            0,            0,              1* theta ^ 0;
      ];

    else
      HR=([
      (cos(theta)),   (-sin(theta)),  0,              0;
      (sin(theta)),   (cos(theta)),   0,              0;
      0,            0,            1,              0;
      0,            0,            0,              1
      ]);
  end
end


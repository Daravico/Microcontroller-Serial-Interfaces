function value = Degree2Percentage(grados, minDeg, maxDeg)

  minPer = 0;

  maxPer = 1;

  m = (maxPer - minPer) / (maxDeg - minDeg);

  value = m * (grados - maxDeg) + maxPer;
end

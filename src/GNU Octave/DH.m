function H = DH(q, l, d, A)
  H = HRz(q) * HTz(l) * HTx(d) * HRx(A);
end


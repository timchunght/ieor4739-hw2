APPL T p
pt 0 <= t < T
rt = (pt-(p(t-1))/pt
rt 1 <= t < T
len(rt) = T - 1
mean = mean(rt)
rt.each do |r|
	r-=mean
end

y-axis = rt
x-axis


objects = cell.o segment.o tif.o nums.o date_and_time.o fit.o fft.o fft_stats.o split_and_overlap.o contiguous.o fl_dist.o align_image.o flatten.o

# -Wall for all compiler warnings messages
# include the paths where you installed tifflib

# Note for windows installation only:
# the CFLAGS should consist of -Wall and a list of include(-I\) 
# and library (-L\) paths, relative to the msys folder, in 
# unix style (i.e. -L\local\include). The include paths should 
# point to the tiffio.h file (-I\local\include) and to glib.h 
# (-I\local\include\glib-2.0). The library paths should point to
# the folder\s that contain libtiff.a and libglib-2.0.dll.a 
# (-L\local\lib).    

CFLAGS = -Wall -static -I/local/include -I/local/include/glib-2.0 -L/local/lib

# the order of the linker commands is important!
cell : $(objects)
	gcc -o cell $(CFLAGS) $(objects) -lm -ltiff -lglib-2.0

cell.o: segment.h tif_routines.h date_and_time.h nums.h point.h image_type.h align_image.h split_and_overlap.h parameters.h file_type.h

tif.o : tif_routines.h

segment.o: segment.h nums.h fit.h tif_routines.h fft_stats.h point.h image_type.h split_and_overlap.h contiguous.h fl_dist.h parameters.h flatten.h

contiguous.o: contiguous.h

nums.o: nums.h tif_routines.h

date_and_time.o: date_and_time.h

fit.o: fit.h

fft.o: fft.h complex.h

fft_stats.o: segment.h fft.h fft_stats.h point.h complex.h

split_and_overlap.o: split_and_overlap.h contiguous.h

fl_dist.o: fl_dist.h contiguous.h

align_image.o: align_image.h

flatten.o: flatten.h

#V1.2a
#oif.o: oif.h

clean:
	rm cell $(objects)


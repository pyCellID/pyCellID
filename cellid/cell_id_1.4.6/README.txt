****************************
This software ("Cell-ID") is being released under the GNU lesser public
license. A copy of the license is in the file
"GNU_Lesser_General_Public_License.txt." The code is
copyright (c) 2005 Andrew Gordon.
****************************

To unpack the tar file, do

tar -zxvf cell_id_1.1

in any directory. A subdirectory cell_id_1.1 will be created.

Two subdirectories are also created in the cell_id_1.1 subdirectory:

paw/ --> contains some scripts relevant to running PAW (which program
         can be downloaded from CERN's website (see below).

example/ --> An example of some images from an experiment and a PAW-readable
             database file.

*******************************************
Outline of the rest of this file:

1) Compiling Cell-ID
2) Running Cell-ID
  a) At the command line
     i)  Images do not have to be time ordered
     ii) First three letters of image names are used to group image types
  b) Input parameters
  c) Dark field correction file
  d) Uneven illumination correction file
  e) Running over multiple position time courses
3) Outputs from Cell-ID
  a) Text files containing all derived information
  b) Annotated images marking boundaries and ID numbers
  c) File containing the time of the earliest image
4) Brief description of code

5) Data analysis package PAW
  a) Getting the code
  b) Formatting the Cell-ID output data into PAW readable file
  c) Basic commands
  d) Some scripts we wrote
  e) Caveats


***************************************
1) COMPILING

The code is written in C, and the Makefile included should be
sufficient to compile it. Just type

  make

at the command line. The code needs libtiff, which is available at
http://www.remotesensing.org/libtiff/ Libtiff is Copyright (c)
1988-1997 Sam Leffler and Copyright (c) 1991-1997 Silicon Graphics,
Inc.

The output of the make command is the executable called "cell."

***************************************
2) RUNNING CELL

The program "cell" can be placed anywhere and run from any
directory. However, there are a number of input files that affect how
it runs.

a) Command line execution

To run, at the command line type

cell  bright_in.txt  fluor_in.txt output_path/output  [third.txt]

The first argument is the name of a text file that contains a list of
images that are used to find the cells (here "bright_in.txt"). The
second argument is the name of a text file that contains a list of
fluorescence images, and the fourht argument is optional and contains
a list of other images that can provide additional information to the
program (such as nuclear tagging).  The third argument is the
"basename" of the output text files, that contains all the information
extracted from the images. If the third argument is, for example,
"output" then the output files will be put in the current directory
and all will begin with the six letters "output".

All images are assumed to be TIF images.

For example, bright_in.txt might contain the following names:
BF_position_1_time0.tif BF_position_1_time1.tif
BF_position_1_time2.tif BF_position_1_time3.tif

and fluor_in.txt might contain YFP_position_1_time0.tif
YFP_position_2_time1.tif YFP_position_3_time2.tif
YFP_position_4_time3.tif

i) In general, the files _do_not_ have to be time ordered. However,
the first thing the program does it to time-sort the images, from
earliest times to latest times. Here it uses one of two pieces of
information to find the time of any image. It first searches the tif
file for Metamorph image tag 33268, which is a tag that Metamorph adds
to tif files to indicate that time of image acquisition. If that isn't
found, then the program uses the time stamp that's built into the tif
image. If this type stamp is the time of  file creation instead of
image formation (as might happen if the user transforms a different
image type into a tif image), then the type information will be
incorrect.

After sorting the images by time, the program will loop through all
the fluorescence images, and then choose the bright field image that
was closest in time to that fluorescence image. It then uses that
bright field image to identify the cells for that fluorescence
image. If the cells have already been found then it doesn't repeat the
procedure. In this way, the program does not require that there is a
1-to-1 correspondence between the bright field and fluorescence
images. There needs to be at least one bright field image, however.

ii) The names of the images in general are arbitrary except for the
first three letters of the name. The program incorporates the
possibility that different types of fluorescence images will be
included in the same experiment by using the first three letters of
the image names. Thus fluor_in.txt might contain
YFP_position_1_time_0.tif CFP_position_1_time_0.tif

and the program will associate a "flag" in the output file to indicate
the different fluorescence images. flag=0 will refer to the earliest
image, flag=1 will refer to the next, etc. (Note that this goes by the
image acquisition times and not the order in the text files.) The
program reports how the flags are associated with the images.

b) parameters.txt: Input parameters are passed to the program through
the file "parameters.txt" The program looks for this file in the
current directory. If it doesn't find a file named "parameters.txt" it
simply uses the defaults for each value. A sample parameters.txt file
is included with the package, and each of the parameters is described
there.

One parameter that might be usefully tweaked is background_reject_factor. The
code makes an initial decision about the graylevels of the boundary pixels. To
do this it takes the mean position of all the graylevels in the images and
subtracts Z standard deviations. It then starts by considering all gray levels
below this value as being parts of the cell borders. This value Z is the
parameter background_reject_factor. Brightfield images taken slightly out of
focus may do better with with higher values (ie, higher values will better
avoid spurious cells), but if the cell boundaries in the image are too narrow,
a smaller value may be necessary--which might increase the level of background.

Another parameter "treat_brightfield_as_fluorescence_also" tells them
program to also treat the bright field image as if it were an additional
fluorescence image. In this case, the bright field image is given flag=0.
This might be a good idea since for one thing it might allow a good way to
reject spurious cells. For example, the average value of the boundary pixels
in good cells will be lower than the background level, but not so for spurious
cells, etc. Thus a cut might be (see the PAW material below):
  (f_m0b/a_m0b-backb)<0.0
to reject some of the spurious cells (assuming that the "b" at the end
of the paw n-tuple variables properly references the bright field image
values). One could make the cut at different levels after
analyzing the different images.

c) dark.txt: The program also searches the current directory for a
file called "dark.txt", which should contain a list of images that
should be subtracted from the fluorescence images. If no dark.txt file
exists then this correction isn't done. The first three letters of the
names in dark.txt indicate which fluorescnece image type they are
associated with. (Even though the shutter may be closed for the dark
image, a YFP image or a CFP image might potentially have different
exposure times.)

d) flat.txt: The program searches for a file called "flat.txt" to use
as a flattening correction. This is for the case that there is uneven
illumination across the image field. The flat.txt file contains a list
of fluorescence images of fields of view that have a uniform
concentration of fluorophores (and therefore _should_ be flat). The
program will attempt to apply a flattening correction to these image
and then to use that correction on the corresponding fluorescence
images of fluor_in.txt.

3) Running over multiple position time courses. Here we consider the situation
that a user has taken many time courses during the same experiments, examining
multiple visual fields and returning to each in sequentially in turn.
Cell should be run separately for each time course. The output of each run
should be placed in a separate directory called "pos1" or "pos2", etc, or
any name the user might choose. The file "time_of_t0.txt" can be used to
connect the timing of each image between the different positions.

**************************************
3) OUTPUTS

There are three types of program outputs.

a) The program makes a series of text files containing different types
of information. If the "basename" passed in as the third argument to
cell at the command line is "output" then the five files will be
output_all output_all_part2 output_all_part3 output_all_part4
output_all_part5 output_all_part6

The current contents of the output files is described in the file
"description_of_output_files.txt"

b) For each image that is read in an annotated image is created. The
anotated image has the same name as the original image except that
phrase ".out.tif" is appended to its name. Thus YFP_position1.tif will
lead to an additional output file YFP_position1.tif.out.tif. These
.out.tif files will be 8 byte tif images and will indicate the borders
of the identified cells and (for bright field images only) the ID
numbers of the cells.

c) The time of the earliest time in the file is appended to the file
"time_of_t0.txt" This file is created if it doesn't exist already. If
exists then the time is appended. The purpose of this file is to allow
for the case that multiple wells in a multi-well plate are being
examined in the same time course, and also for the case that multiple
visual field positions are examined in the same well. Thus, for
example, if well 1 is a time course and there are five visual fields
examined sequentially at each time step, then time_of_t0.txt can be
used to put all that information together.

**************************************
4) CODE DESCRIPTION

Here is a brief description of salient features of the code.

In cell.c (which contains main()), the program reads in each of the
files in fluor_in.txt and bright_in.txt and time sorts them. It then
loops over each of the fluorescence images and uses the nearest-time
bright field image to identify the cells. As described
above, it analyses the first three letters of the fluorescence image
names to determine whether those images should be given a new "flag."
This flag is appended to the output files. 

To find the cells, control is passed to the routine find_cells(), which can
be found in segment.c.

The file segment.c contains most of the image-analysis routines. These
routines make use of a number of variables that are global to this
file. Indeed, the bright field and fluorescence images are global to
the file. These arrays are passed from cell.c to segment.c through the
routine "load_global_arrays."  (Thus, one must be careful in cell.c
that the right arrays have been sent to the routines in segment.c--and
haven't been changed unexpectedly by additional code, etc.)

The boundary pixels and interior pixels to each cell are stored as
linked lists of integer coordinates (defined by struct point). 
For each cell, the arrays boundary[i] and interior[i] are pointers to
the start of the linked lists for the boundary and interior pixels for cell
number i. These
arrays are global to the segment.c file.
Similarly, the different variables that
get associated with each newly found cells are stored in arrays that are
global to segment.c. For example, vol_rotation[i] will contain the
volume of rotation of the ith cell, etc.

After calling find_cells(),
the program calculates a number of variables associated with the
fluorescence images through the routine
calculate_fluorescence_with_r_info(), which is also in segment.c. The
various statistics here are also stored in global arrays.

After examining a given fluorescence image, the program attempts to
"track" the cells through a time course. This is done in
update_list_of_found_cells(). This routine compares each of the cells
that were found in the latest bright field image to all the cells found
in previous
images and calculates an overlap between the cells. If the overlap for a
given cell with another cell in a previous time point is
good enough then it associates all the information for the new
cell with the previous cell. Thus for example, if ith cell that was
found in the current bright field image shows a good match with ID 44
of the previous image, then the ith cell will be given ID number 44
and its information appended to the information for ID 44. If there is
no good match, then the current cell will be given a new ID
number. 

After this cell tracking step, 
the data for all the cells is stored in a segment.c global array
called cs[]. cs[i] is a pointer to a linked list of structures 
of type "blob" where
the structure type blob is defined in segment.c and simply contains
all the information that had been accumulated in the segment.c global
arrays, such as vol_rotation[], etc. Each ID number is associated with its
own linked list of blob structures, and each element in the list
contains all the information for a given time point.
For example, cs[0]->index contains the ID
number of the first cell found. This array is set up so that
cs[0]->index points to the information from the last time point in
which that ID number was associated with a cell.  The information from
the first time point for this cell can be found from

  struct blob *b;
  for(b=cs[0];b->prev!=NULL;b=b->prev) ;

b will then be a pointer to the "blob" information for the first
cell. To add new variables for each cell, an addition to the blob
structure has to be made.

All the blob structure information is outputted in the routine
output_cells().

**************************************
5) DATA ANALYSIS PACKAGE PAW

PAW stands for Physics Analsis Workstation and is a data analysis and plotting
package put out by CERN. 

The program Cell is independent of PAW, but we have included in the package
some PAW scripts that help in re-formatting the text output data into a
PAW-usable file.

All the PAW scripts are in the sub-directory paw/ of the release.

An example ntuple is given in example/nt.hst.

a) Getting started

PAW is available for download at

http://wwwasd.web.cern.ch/wwwasd/paw/

It can be run from the command line.

A start-up file is needed to use some of the scripts we wrote. In
particular, edit the file

.pawlogon.kumac

in your home area (for unix). And add the lines

macro/defaults '.,[directory where general paw scripts are]'
global/create flpaw '[directory where general paw scripts are]'

where "[directory where general paw scripts are]" is the complete path
to the location where any number of paw scripts are kept (the paw scripts all
contain ".kumac" at the end). For the "macro/defaults" line, the period
in the first position indicates that PAW should first look in the current
directory for any scripts and then in the indicated directory if it doesn't
findthemt in the current directory.

Some of the scripts we wrote make use of the "flpaw" variable to tell the
program where to find other scripts.

b) Formatting output files into paw readable files ("n-tuple").

An example experiment and its n-tuple are included in the subdirectory
example/.

The PAW readable tabulated information is referred to as an "n-tuple". The
script read.kumac (and some supporting scrips), runs over the output files
and re-formats them into an n-tuple.

read.kumac makes assumptions about how the directories are set up to find
the data. Specifically, it assumes the following directory setup:

"top-directory" contains:
   Text files describing experiment (or anything else user wants), and
   a subdirectory called images/

   images is a subdirectory that contains all the image data.
   It also contains a series of subdirectories
   pos1/
   pos2/
   pos3/
   .
   .
   .
   posn/

   where each subdirectory pos1, pos2, etc, contains the output files for
   the cell run over each position.

(If a name other than pos1, pos2, etc, is used, the relevant line in read.kumac
can simply be changed. That line is

exec output_to_ntuple_[tyc] 1 [h] pos 1 [n] output_all [etime] [max_t]

and the letters "pos" should indicate the prefix of the output subdirectories
in the images subdirectory.

However, read.kumac does assume that positions are sequential.)

read.kumac also assumes that there is a file called "time_of_t0_cor.txt"
which contains the time of the first image for each position. If this file
does not exist, then the file will not run correctly. To make this file,
simply edited time_of_t0.txt and subtract the smallest number from each time,
so that the times start at 0. Alternatively, you could just rename
time_of_t0.txt to time_of_t0_cor.txt, which would work fine, but the absolute
value of the times in the PAW ntuple would not be easily interpreted.

To run read.kumac script, copy the file read_par.kumac to the top-directory
of the experiment (ie, just above the images subdirectory). This is where
paw should be run from.

This file defines three necessary variables (the paw command to create
the variables is "global/create"). For example:

global/create in_num 20
global/create in_tmx YC
global/create in_nuc 9

The 20 indicates that for this experiment there are 20 positions
to run over. The in_tmx is a string where each character labels the
different colors. For the example, YC means that flag=0 corresponds to
YFP images and flag=1 corresponds to C images. Note that the correspondence
of the flag number to the image color type is determine by the actual time
of the image files. This information is printed out by cell during the run.
For this example, every variable name in the ntuple that is associated with
the YFP image will have a Y added to it, and every CFP variable a C.
The 9 indicates the version number to use for the scripts making the ntuple.
Currently only 9 is included in the relase.

Note that if you ran with the option to treat the bright field image as
a fluorescence image, then you will have flag=0 corresponding to the
bright field data (as if it were a fluorescence image). Then, for the example
above in_tmx should be BYC.

To make the ntuple, type

PAW> exec read

at the PAW> prompt after starting PAW. A series of messages should go by of
the form "vector created with certain length", and the PAW prompt should
return after the script is finished. Type

PAW> nt/print 3

and then exit.

(The nt/print 3 shouldn't be necessary but seems to be. It seems that if
the ntuple isn't actually accessed before quitting, then it doesn't save
correctly).

At this point, you should have a potentially large file called tmp.hst
sitting in the directory that PAW was run from. Every time exec read is
done, this file is over-written. Therefore, you should rename this file to
something else. For example:
 mv tmp.hst nt.hst

c) Basic PAW commands

First start PAW from the command line.

To load and run a file (in this case nt.hst):

PAW> hist/file 1 nt.hst

read.kumac created an ntuple with the label "3". (Earlier versions had
ntuples 1 and 2 for different purpose but which aren't used any longer.)

To examine the variable names:

PAW> nt/print 3

The resulting table indicates all the "columns" that are stored in the
ntuple. If there is a multi-colored experiment (for example with YFP and
CFP images, and in_tmx above was set to YC, for example), then every variable
with a Y after it refers to the YFP data, and every variable with a C to the
CFP data.

For the YFP information, you might see something like this:

 ******************************************************************
 * Var numb * Type * Packing *    Range     *  Block   *  Name    *
 ******************************************************************
 *      1   * R*4  *         *              * DATA-Y   * posY
 *      2   * R*4  *         *              * DATA-Y   * n_totY
 *      3   * R*4  *         *              * DATA-Y   * idY
 *      4   * R*4  *         *              * DATA-Y   * i_tY
 *      5   * R*4  *         *              * DATA-Y   * tY
 *      6   * R*4  *         *              * DATA-Y   * x0Y
 *      7   * R*4  *         *              * DATA-Y   * y0Y
 *      8   * R*4  *         *              * DATA-Y   * flrawY
 *      9   * R*4  *         *              * DATA-Y   * bck5Y
 *     10   * R*4  *         *              * DATA-Y   * ause5Y
 *     11   * R*4  *         *              * DATA-Y   * areaY
 *     12   * R*4  *         *              * DATA-Y   * fftY
 *     13   * R*4  *         *              * DATA-Y   * i_t0Y
 *     14   * R*4  *         *              * DATA-Y   * a_vacY
 *     15   * R*4  *         *              * DATA-Y   * f_vacY
 *     16   * R*4  *         *              * DATA-Y   * backY
 *     17   * R*4  *         *              * DATA-Y   * circY
 *     18   * R*4  *         *              * DATA-Y   * majorY
 *     19   * R*4  *         *              * DATA-Y   * minorY
 *     20   * R*4  *         *              * DATA-Y   * f_nucY
 *     21   * R*4  *         *              * DATA-Y   * a_nucY
 *     22   * R*4  *         *              * DATA-Y   * flagY
 *     23   * R*4  *         *              * DATA-Y   * vconY
 *     24   * R*4  *         *              * DATA-Y   * volY
 *     25   * R*4  *         *              * DATA-Y   * f_p1Y
 *     26   * R*4  *         *              * DATA-Y   * a_p1Y
 *     27   * R*4  *         *              * DATA-Y   * bckmY
 *     28   * R*4  *         *              * DATA-Y   * ausemY
 *     29   * R*4  *         *              * DATA-Y   * f_m0Y
 *     30   * R*4  *         *              * DATA-Y   * a_m0Y
 *     31   * R*4  *         *              * DATA-Y   * atot5Y
 *     32   * R*4  *         *              * DATA-Y   * atotmY
 *     33   * R*4  *         *              * DATA-Y   * f_m1Y
 *     34   * R*4  *         *              * DATA-Y   * a_m1Y
 *     35   * R*4  *         *              * DATA-Y   * veff1Y
 *     36   * R*4  *         *              * DATA-Y   * veff2Y
 *     37   * R*4  *         *              * DATA-Y   * f_m2Y
 *     38   * R*4  *         *              * DATA-Y   * a_m2Y
 *     39   * R*4  *         *              * DATA-Y   * veff3Y
 *     40   * R*4  *         *              * DATA-Y   * veff4Y
 *     41   * R*4  *         *              * DATA-Y   * f_m3Y
 *     42   * R*4  *         *              * DATA-Y   * a_m3Y
 *     43   * R*4  *         *              * DATA-Y   * veff5Y
 *     44   * R*4  *         *              * DATA-Y   * saY
 ******************************************************************

Here's a description of each these variables (see also
"description_of_output_files.txt").
posY--position number
n_totY--total number of time frames in which this cell was found
idY--id number
i_tY--time frame number (starts at 0)
tY--time in seconds from start of experiment
x0Y--centroid x
y0Y--centroid y
flrawY--total fluorescence
bck5Y--background average at location 5 pixels from cell boundary
ause5Y--number of pixels a 5 pixels away from cell boundary not associated with        any othe rcell
areaY--number of pixels in the cell
fftY--circularity statistic based on FFT of radius vs angle of boundary pixels
i_t0Y--time frame number in which this cell was first found
a_vacY--area of vacuole as determined from darker fluorescence regions
f_vacY--total fluorescence of those pixels 
backY--mode of pixel distribution of pixels not associated with a cell
circY--circumference of cell
majorY--major axis
minorY--minor axis
f_nucY--nuclear fluorescence if nucleus was labelled
a_nucY--area of nuclues
flagY--flag associated with this type of color image
vconY--volume using "conical" method
volY--volume using "volume of spheres" method
f_p1Y--total fluorescence in annulus one pixel outside cell boundary
       (this is different than what is the output file, which contains
       the total within this annulus). Here it just the fluorescence along
       the annulus.
a_p1Y--number of pixels along this annulus
bckmY--like bck5Y but going out half the minor axis instead of 5 pixels
ausemY--like ause5Y but going out half the minor axis
f_m0Y--total fluorescence in annulus along cell boundary (see
       comment about f_p1Y) above
a_m0Y--total pixels along this annulus
atot5Y--total number of pixels along annulus a 5 pixels outside cell boundary
atotmY--same as atot5Y but going out half the minor axis
f_m1Y--same as f_p1Y but for annulus one pixel inside boundary
a_m1Y--same as a_p1Y but for annulus one pixel inside boundary
veff1Y--not used
veff2Y--not used
f_m2Y--same as f_p1Y but for annulus two pixels inside boundary
a_m2Y--same as a_p1Y but for annulus two pixels inside boundary
veff3Y--not used
veff4Y--not used
f_m3Y--total fluorescence for all pixels inside of and including an annulus
       3 pixels inside boundary (Thus f_m3Y+f_m2Y+f_m1Y+f_m0Y=flrawY)
a_m3Y--number of pixels interior to and including an annulus 3 pixels inside
       bondary (thus a_m3Y+a_m2Y+a_m1Y+a_m0Y=areay)
veff5Y--not used
saY--surface area measurement, although not particularly to be trusted at this
     point.

Note that this data structure wastes space. For example, n_totY is the total
number of time points that a give cell was found in. This value is stored in
the rows for each of the time points for that cell, even though it is the 
same value. Similarly, for idy, i_t0y, etc.

Making plots:

To make a histogram of the data, do

PAW> nt/plot 3.flrawy

which will histogram the total fluorescence of all the cells for all the time,
for the YFP channel.

To see some summary statistics of the histogram, do

PAW> opt stat

to turn have the statistics printed out on top of the histogram (for
the next histogram plotted), and

PAW> opt nstat

to turn the option off.

To restrict the plot to time 0, do 

PAW> nt/plot 3.flrawy i_t0y=0.0

Cell-ID will sometimes produce spurious cells, one can attempt to characterize
them in a number of ways. To remove cells based on having weird shapes, or
small sizes, try

PAW> nt/plot 3.flrawy i_t0y=0.0.and.ffty<0.3.and.areay>200.0

Note that ".and." that separates that different cuts.

To make a 2d plot, the "vs" command is a percentage sign. Like so:

PAW> nt/plot 3.flrawy%i_ty ffty<0.3.and.areay>200.0

Note that the "cuts" ffty<0.3.and.area>200.0 are applied separately at each
time point. For this example PAW will loop over all the data in the ntuple,
and examine ffty and areay separately at each time point. Say cell number 1
passes the cuts for i_ty=0 and 3, but fail it for the other time points. Then
cell number 1 will only appear in the 0th and 3rd time frame for that plot.
This might not be the behavior that was desired.

To get around this, we created some paw scripts that create "vectors" that
can be accessed with the nt/plot command. The script

PAW> exec fixed_tvec3

picks out the information for a given time point. For example

PAW> exec fixed_tvec3 0 ffty ffty0

will create a vector called ffty0() that contains the time 0 values of
ffty. The script also creates a paw "variable" that can be directly
accessed with the nt/plot command. This variable is accessed by putting
hard brackets around the name "ffty0".

Thus,

PAW> exec fixed_tvec3 0 ffty ffty0
PAW> exec fixed_tvec3 0 areay areay0
PAW> nt/plot 3.flrawy%i_ty [ffty0]<0.3.and.[areay0]>200.0

will make a plot of flrawy vs frame number for cells which passed the
areay and ffty cuts in the first frame only.

To simplify the cuts, one can define cut variables as

PAW> nt/cut 1 ([ffty0]<0.3.and.[areay0]>200.0)

etc

The cuts are accessed with a $ in front of the number. So the above
plotting command is equivalent to

PAW> nt/plot 3.flrawy%i_ty $1

In general, elementary calculations can be done at the command line. For
example,
PAW> nt/plot 3.flrawy/areay%i_ty $1

will plot the total fluorescence per pixel vs frame number.

See 

PAW> help nt/plot
for other options

To make histograms of fixed sizes, see

PAW> help 1d
or
PAW> help 2d

To fill these histograms, see

PAW> help nt/project


d) Some scripts we wrote.

PAW> exec fixed_tvec3

extacts all the data for a given time point. Note that if one were to do

PAW> exec fixed_tvec3 0 areay a0

followed by

PAW> nt/plot 3.[a0]

then PAW would make a histogram of the values of areay for the first time
point, but it would do this over and over again, for each of the time points
in the experiment. That is, the histogram would have the identical shape
as the command

PAW> nt/plot 3.areay i_ty=0.0

but it would have N times as many data points. This can produce spurious
standard errors.

An example of a useful way to use this command is to, for example, compare
the last time point to the first. For example,

PAW> exec fixed_tvec3 0 flrawy/areay fa0
PAW> exec fixed_tvec3 10 flrawy/areay fa10

(if there are 11 time points (i_ty from 0 to 10)). The command

nt/plot 3.[fa10]%[fa0] n_toty>10.0.and.i_ty=10.0

will then produce a plot of time 10 vs time 0.

The script

PAW> exec old_stats_med

will calculate the median and standard deviation (based on the median
of the absolute deviations) of the data. This is potentially a more
robust (although not necessarily unbiased) way of estimating the means
and standard deviations of a data set.

The script

PAW> exec stats_med

will do the same as old_stats_med but in a way that is faster and can
handle much larger data sets. This second method, does the calculation
in a C program called get_median_and_mad.c (included in the paw directory
of the release). One should compile this with any c compiler into the
executable get_median_and_mad to make use of this feature.

PAW> exec old_cov_matrix

uses the "bi-weight" to calculate the covariance matrix, and

PAW> exec cov_matrix

does the same but with a C routine. For this, you need to compile the
code get_biwt.c into an executable called get_biwt.

e) Caveats
   i) When accessing the disk (such as with hist/file 1 nt.hst), PAW will
      pass the file name to the system in all lower case, although it won't
      tell you this. If your file system is case sensitive, then you might
      find it impossible to load a file named Exp1.hst. Keeping all names
      lower case solves this problem.
 
  ii) If a script creates new PAW variables, those variables will
      automatically be visible at the command line. However, if one scripts
      calls another script, the variables created in the second script will
      not automatically be available in the first, even if they are declared
      "global." To make them available, do
      global/import *







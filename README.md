# bdkit
Python tool interface with VASPkit. This allow you to plot band and DOS.

In order to use this tool you have to install:
Vaspkit: https://vaspkit.com/
Python3

Matplolib

Numpy

Pandas


pip3 install numpy pandas matplotlib 

Then you need the file generate by vaspkit.

First make one directory name band_dos go inside and create band and dos directories and make the appropriate calculation using vaspkit.

When you have your results, you can generate using VASPKIT, the data needed for the plot of band and DOS.

For band at the PBE level you have to use the next commands:

        vaspkit -task 211 -file POSCAR

        vaspkit -task 213 -file POSCAR

For band at the metaGGA or hybrid functional level:

      vaspkit -task 303 -file POSCAR

      vaspkit -task 252 -file POSCAR

      vaspkit -task 254 -file POSCAR

For dos at all level:

      vaspkit -task 111 -file POSCAR

      vaspkit -task 113 -file POSCAR

These commands will generate different files.

For the band calculation that will generate files of each elements in your system with the information of the projected band. For the KN8 structure that will generate the files:

BAND.dat    PBAND_K.dat  PBAND_N.dat 

Where BAND.dat contain the full band structure, PBAND_K.dat contain the projection of the K element over the band structure and PBAND_N.dat contain the projection of the N element over the band structure.

The same kind of files will be obtain for the DOS. For the KN8 structure that will generate the files:

PDOS_K.dat		TDOS.dat	PDOS_N.dat 

Where TDOS.dat contain the full DOS, PDOS_K.dat contain the projected DOS of the K element and PDOS_N.dat contain the projected DOS of the N element.

Then we use these files to plot the BAND-DOS plot. For that one can use the script bdkit.

To install the bdkit, you have to download all the files and put bdkit in your path.


Then you can use it: 

bdkit -h

usage: BDkit1.0 [-h] [-t TITLE] [-lf LABELFIG] [-xl XLEGEND] [-yl YLEGEND] [-fsize FONTSIZE]

                [-xrot XROTATION] [-emin EMIN] [-emax EMAX] [-dpi DPI]
                
                kindatm typeatm typeorb colors

positional arguments:

  kindatm               number of the different elements in your compound
  
  typeatm               name of the elements in this way 'N,O'
  
  typeorb               label of the orbitals in this way 's,p;d
  
  colors                color of the orbitals, same lenght as the typeorb, 'blue,red;green'
  

optional arguments:

  -h, --help            show this help message and exit
  
  -t TITLE, --title TITLE
  
                        title of the figure, default nothing
                        
  -lf LABELFIG, --labelfig LABELFIG
  
                        label of the figure, default nothing
                        
  -xl XLEGEND, --xlegend XLEGEND
  
                        x position of the legend, default 1.1
                        
  -yl YLEGEND, --ylegend YLEGEND
  
                        y position of the legend, default 0.95
                        
  -fsize FONTSIZE, --fontsize FONTSIZE

                        font size, default 19
                        
  -xrot XROTATION, --xrotation XROTATION
  
                        rotation of the k-path, default 0
                        
  -emin EMIN, --emin EMIN
  
                        minimum energie, default -8.0
                        
  -emax EMAX, --emax EMAX
  
                        maximum energie, default 6.0
                        
  -dpi DPI, --dpi DPI   
  
                        value of the image dpi, default 400
  

  

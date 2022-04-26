// Stores Image ID
idImage=getImageID();
run("Clear all");
//open("C:/Users/shil5659/Dropbox/DPhil/2021/image-analysis/napari/nuclei_labels_2.csv");
open("C:/Users/shil5659/Dropbox/DPhil/2021/image-analysis/cell_shape_experiments/output/nuclear_segs/img_1_tmp_df.csv")
Table.rename("img_1_tmp_df.csv", "Results");
z_scale = 0.25
roiManager("reset");
for (i=0;i<nResults;i++) {
	xp=getResult("centroid-2", i);	
	yp=getResult("centroid-1", i);	
	zp=getResult("centroid-0", i); // * z_scale; //centroid_z is in pixels not frames
	radius = getResult("equivalent_diameter_area", i)*0.5; //mean d makes more sense but cant measure atm
	//radius = getResult("mean_distance_to_centroid", i); 
	setSlice(zp+1);	
	makeOval(xp-radius,yp-radius,2*radius,2*radius);
	Roi.setPosition(1, zp+1, 1);
	roiManager("Add");
}
// Prepare to work on the initial CElegans image
selectImage(idImage);

// below is OK 
// run("Sphere Seg", "d_0=6 f_pressure=0.005 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.133");

// first try using biological parameters
// this is OK - some cells don't fill the whole space 
// run("Sphere Seg", "d_0=6 f_pressure=0.005 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.076");


// try increasing f_pressure to get cells bigger 
// leaves too many open spaces- try also decreasing d_0
// run("Sphere Seg", "d_0=6 f_pressure=0.01 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.076");


// now it is very slow! 
// too many gaps in cells 
// so increase d0? 
// run("Sphere Seg", "d_0=3 f_pressure=0.01 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.076");

// oh yea a median 3d = 5 filter seems to help? 


// really really coarse but possibly salvagable?  I think the detail thats there is more accurate
run("Sphere Seg", "d_0=9 f_pressure=0.01 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.076");


log('done'); 
// trying increased fpressure tho 
// run("Sphere Seg", "d_0=6 f_pressure=0.015 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.076");


// wonder if this is better now my cell boudnaries are so thick 
// did CAHE then median filter 
// no :) that really doesn't work 
// run("Sphere Seg", "d_0=3 f_pressure=0.01 z_scale=3.2 range_in_d0_units=1.5 samecell=false show3d=true numberofintegrationstep=-1 realxypixelsize=0.076");






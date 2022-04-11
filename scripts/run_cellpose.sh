
python -m cellpose --dir ../data/nuclei_images/ \
--pretrained_model nuclei \
--diameter 100 \
--save_tif \
--chan 0 \
--do_3D \
--savedir /mnt/c/Users/shil5659/Dropbox/DPhil/image-analysis/cell_shape_experiments/output/ \
--anisotropy 3.2892183369975223 \
--verbose \
--batch_size 1 \
--no_resample # we don't need high resolution and this will speed up tons

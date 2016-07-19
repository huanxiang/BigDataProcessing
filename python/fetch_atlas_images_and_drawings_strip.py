import urllib, json
import os
from PIL import Image
import numpy as np

#
# See also:
# http://help.brain-map.org/display/api/Atlas+Drawings+and+Ontologies
#

# Specify output directory for images
output_directory = "output"
if not os.path.exists( output_directory ) :
    os.makedirs( output_directory )
# Specify downsample factor
downsample = 0

# Atlases
gyral_atlas = 138322605 	
brodmann_atlas = 265297126

# graphic layers
gyral_layers = "31,113753815,113753816,141667008"
brodmann_layers = "31,113753816,141667008,265297118" 

# download ontology file
query_url = "http://api.brain-map.org/api/v2/structure_graph_download/16.json"
ontology_path = os.path.join( output_directory, "structure_ontology.json" )
#urllib.urlretrieve(query_url, ontology_path)

# RMA query to find images for atlas
query_url = "http://api.brain-map.org/api/v2/data/query.json?criteria=model::AtlasImage,rma::criteria,[annotated$eqtrue],atlas_data_set(atlases[id$eq265297126]),alternate_images[image_type$eq'Atlas+-+Developing+Human+Brodmann'],rma::options[order$eq'sub_images.section_number'][num_rows$eqall]"

response = urllib.urlopen(query_url)
images = json.loads(response.read())['msg']

# making output directories
nissl_directory = os.path.join(output_directory,'nissl')
if not os.path.exists( nissl_directory ) :
    os.makedirs( nissl_directory )
    
brodmann_atlas_directory = os.path.join(output_directory,'brodmann_atlas')
if not os.path.exists( brodmann_atlas_directory ) :
    os.makedirs( brodmann_atlas_directory )
    
brodmann_svg_directory = os.path.join(output_directory,'brodmann_svg')
if not os.path.exists( brodmann_svg_directory ) :
    os.makedirs( brodmann_svg_directory )
    
gyral_svg_directory = os.path.join(output_directory,'gyral_svg')
if not os.path.exists( gyral_svg_directory ) :
    os.makedirs( gyral_svg_directory )

num_block_x = 10
num_block_y = 10

# loop through each image
index = 0
for i in images :
    
    if index >=0 and index < 10:
        print i['section_number']
        
        # Query image dimentsion
        image_height = i['image_height']
        image_width = i['image_width']
        
        block_size_x = image_width / num_block_x
        block_size_y = image_height / num_block_y
        residual_x = image_width % num_block_x
        residual_y = image_height % num_block_y
        
        for x in range(num_block_x):
            for y in range(num_block_y):
                
                print('processing block '+str(x)+' '+str(y))
                
                if x == num_block_x - 1:
                    current_block_size_x = block_size_x + residual_x
                else:
                    current_block_size_x = block_size_x
                if y == num_block_y - 1:
                    current_block_size_y = block_size_y + residual_y
                else:
                    current_block_size_y = block_size_y
                
                left = x * block_size_x
                top = y * block_size_y
                image_url  = "http://api.brain-map.org/api/v2/section_image_download/%d?left=%d&top=%d&width=%d&height=%d" % (i['id'],left,top,current_block_size_x,current_block_size_y)    
                image_path = os.path.join( nissl_directory, '%04d_%d_%d.jpg' % (i['section_number'], x,y)    )
                if os.path.isfile(image_path):
                    continue 
                while True:
                    try:
                        urllib.urlretrieve(image_url, image_path)
                        break
                    except IOError:
                        print IOError
                        pass
                
        
        # downsampled images 
#         image_url  = "http://api.brain-map.org/api/v2/section_image_download/%d?downsample=%d" % (i['id'],downsample)
#         image_path = os.path.join( nissl_directory, '%04d.jpg' % i['section_number']    )
#         urllib.urlretrieve(image_url, image_path)
    
#         image_url  = "http://api.brain-map.org/api/v2/atlas_image_download/%d?downsample=%d&annotation=true&atlas=%d" % (i['id'],downsample,brodmann_atlas)
#         image_path = os.path.join( brodmann_atlas_directory, '%04d.jpg' % i['section_number']    )
#         urllib.urlretrieve(image_url, image_path)
#         
#         # download svg
#         svg_url = "http://api.brain-map.org/api/v2/svg_download/%d?groups=%s&downsample=%d" % (i['id'],gyral_layers,downsample)
#         svg_path = os.path.join( gyral_svg_directory, '%04d.svg' % i['section_number']    )
#         urllib.urlretrieve(svg_url, svg_path)
#         
#         svg_url = "http://api.brain-map.org/api/v2/svg_download/%d?groups=%s&downsample=%d" % (i['id'],brodmann_layers,downsample)
#         svg_path = os.path.join( brodmann_svg_directory, '%04d.svg' % i['section_number']    )
#         urllib.urlretrieve(svg_url, svg_path)
    
    index += 1

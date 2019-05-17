#!/usr/bin/python
# import the python renderman library
from __future__ import print_function
import sys
import sys,os.path,subprocess
import prman
import ProcessCommandLine as cl

	# Main rendering routine
def main(filename,shadingrate=10,pixelvar=0.1,
         fov=0,width=1920,height=1080,
         integrator='PxrPathTracer',integratorParams={}
        ) :
	print ("shading rate {} pivel variance {} using {} {}".format(shadingrate,pixelvar,integrator,integratorParams))
	ri = prman.Ri() # create an instance of the RenderMan interface

		# this is the begining of the rib archive generation we can only
		# make RI calls after this function else we get a core dump
	ri.Begin(filename)
	ri.Option('searchpath', {'string archive':'./assets/:@'})
#	ri.Option('searchpath', {'string texture':'../Textures/:@'})

		# now we add the display element using the usual elements
		# FILENAME DISPLAY Type Output format
	ri.Display('rgb.exr', 'it', 'rgba')
	ri.Format(width,height,1)

		# setup the raytrace / integrators
	ri.Hider('raytrace' ,{'int incremental' :[1]})
	ri.Integrator('PxrPathTracer','integrator')
	ri.ShadingRate(shadingrate)
	ri.PixelVariance (pixelvar)
		#ri.Integrator (integrator ,'integrator',integratorParams)
	ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
	ri.Option( 'statistics', {'endofframe' : [ 1 ] })
	ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})
	ri.DepthOfField(0, 0, 10)


	# now we start our world
	ri.WorldBegin()

	###############**CAMERA**#######################
	ri.Rotate(-90,1,0,0)
	#ri.Rotate(-4,1,0,0)
	#ri.Rotate(-90,1,0,0)
	ri.Translate(0,-11,-1.7)
	################################################

	################**LIGHTING**####################
	ri.AttributeBegin()
	#ri.Rotate(-90,0,1,0)
	ri.Light('PxrDomeLight','sceneLight',
	{
		'string lightColorMap' : 'bathroom_4k.tx'
	})

	ri.AttributeEnd()
	################################################

	###############**BOTTLE BOTTOM**################
	# ri.AttributeBegin
	# ri.Pattern('PxrFlakes','goldFlakes',
	# {
	# 	'normal inputNormal' : [0,0,0], 
	# 	'float flakeAmount' : [.5], 
	# 	'float flakeFreq' : [57.30], 
	# 	'float density' : [1.0], 
	# 	'float size' : [1.0], 
	# 	'int octaves' : [1], 
	# 	'float jitter' : [0.75], 
	# 	'int validateNormals' : [0], 
	# })

	ri.Pattern('band','band', { })

	ri.Bxdf('PxrSurface','baseMaterial',
	{ 
		'reference color diffuseColor' : ['band:Cout'],
		'color specularFaceColor' : [0.2,0.2,0.2], 
		'color specularEdgeColor' : [0.2,0.2,0.2],
		'float specularRoughness' : [0.1],
	})
	ri.Cylinder (1.2,-2,2,360)
	ri.AttributeEnd
	#################################################

	##################**BASE TOP**###################
	ri.TransformBegin()
	ri.Translate(0,0,2)

	ri.AttributeBegin
	ri.Pattern('flakes','flakes', { })
	# ri.Pattern('PxrFlakes','goldFlakes',
	# {
	# 	'normal inputNormal' : [0,0,0], 
	# 	'float flakeAmount' : [1000], 
	# 	'float flakeFreq' : [57.30], 
	# 	'float density' : [1.0], 
	# 	'float size' : [4.0], 
	# 	'int octaves' : [1], 
	# 	'float jitter' : [0.75], 
	# 	'int validateNormals' : [0], 
	# })

	ri.Bxdf('PxrSurface','baseMaterial',
	{
		'color diffuseColor' : [0.202,0.131,0.233], 
		'color specularFaceColor' : [0.2,0.2,0.2], 
		'color specularEdgeColor' : [0.2,0.2,0.2],  
		'float specularRoughness' : [0.1],
	})
	# ri.AttributeEnd
	ri.Sphere (1.2,0,0.95,360)
	##################################################

	##################**CAP**#########################
	ri.TransformBegin()
	ri.Translate(0,0.01,1.9)
	ri.Bxdf('PxrSurface','capMaterial',
	{ 
		'color diffuseColor' : [0.324000001, 0.297077745, 0.257580012], 
		'color specularFaceColor' : [0.324000001, 0.297077745, 0.257580012], 
		'color specularEdgeColor' : [0.324000001, 0.297077745, 0.257580012],
		'float specularRoughness' : [0.0],   
	})
	ri.Cylinder (0.7,-0.9,0.9,360)
	ri.TransformEnd()
	ri.TransformEnd()
	#####################################################

	###################**TABLE**#########################
	ri.AttributeBegin()
	ri.Pattern('PxrTexture','wood',
	{
		'string filename' : ['wood2.tx'], 
	})
	
	ri.Bxdf('PxrDisney', 'table', 
	{ 
		'reference color baseColor' : ['wood:resultRGB'],
	})

	ri.Patch('bilinear', {ri.P: [-9, -3, -2, -9, 3, -2, 9, -3, -2, 9, 3, -2]})
	ri.AttributeEnd()
	#####################################################

	# end our world
	ri.WorldEnd()
	# and finally end the rib file
	ri.End()

def checkAndCompileShader(shader) :
	if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
	#print 'compiling shader %s'%(shader)
		try :
				subprocess.check_call(['oslc', shader+'.osl'])
		except subprocess.CalledProcessError :
				sys.exit('shader compilation failed')

if __name__ == '__main__':  
	checkAndCompileShader('band')
	checkAndCompileShader('flakes')
	cl.ProcessCommandLine('testScenes.rib')
	main(cl.filename,cl.args.shadingrate,cl.args.pixelvar,cl.args.fov,cl.args.width,cl.args.height,cl.integrator,cl.integratorParams)
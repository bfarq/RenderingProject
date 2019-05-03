# import the python renderman library
import prman

ri = prman.Ri() # create an instance of the RenderMan interface
filename = "__render" # "Spray.rib"

# this is the begining of the rib archive generation we can only
# make RI calls after this function else we get a core dump
ri.Begin('__render')

# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatenate output
ri.ArchiveRecord(ri.COMMENT, 'Comments start with a #')

# now we add the display element using the usual elements
# FILENAME DISPLAY Type Output format
ri.Display("spray.exr", "it", "rgba")

# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(720,576,1)

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:60}) 

# now we start our world
ri.WorldBegin()

ri.Rotate(-90,1,0,0)
ri.Translate(0,-8,-1)

############################################################################
#LIGHT: Will add Dome light and indoor Environment Map later
ri.AttributeBegin()
ri.Light('PxrEnvDayLight','light1',
{
   'float intensity' : [3.0],
})
ri.AttributeEnd()
############################################################################

############################################################################
#BottleBottom
ri.Bxdf('PxrSurface','baseMaterial',
{
	'float diffuseGain' : [1.0], 
	'color diffuseColor' : [.700,.588,.420], 
	'float diffuseRoughness' : [0.0],
	'color specularFaceColor' : [0,0,0], 
	'color specularEdgeColor' : [0,0,0], 
	'color specularExtinctionCoeff' : [0.0,0.0,0.0], 
	'float specularRoughness' : [0.2], 
})
ri.Cylinder (1.2,-2,2,360)

ri.TransformBegin()
#BaseTop
ri.Translate(0,0,2)
ri.Bxdf('PxrSurface','baseMaterial',
{
	'float diffuseGain' : [1.0], 
	'color diffuseColor' : [0.202,0.131,0.233], 
	'float diffuseRoughness' : [0.0],
	'color specularFaceColor' : [0,0,0], 
	'color specularEdgeColor' : [0,0,0], 
	'color specularExtinctionCoeff' : [0.0,0.0,0.0], 
	'float specularRoughness' : [0.2], 
})
ri.Sphere (1.2,0,0.95,360)

ri.TransformBegin()
#Cap
ri.Translate(0,0.01,1.9)
ri.Bxdf('PxrSurface','metal',
{
	'float diffuseGain' : [1.0], 
	'color diffuseColor' : [0.2,0.2,0.2], 
	'float diffuseRoughness' : [0.0],
	'color specularFaceColor' : [0.18,0.18,0.18], 
	'color specularEdgeColor' : [0,0,0], 
	'float specularFresnelShape' : [5.0],
	'color specularExtinctionCoeff' : [0.0,0.0,0.0], 
	'float specularRoughness' : [0.5],
	'color roughSpecularFaceColor' : [0,0,0], 
	'color roughSpecularEdgeColor' : [0,0,0], 
	'float roughSpecularFresnelShape' : [5.0], 
	'color roughSpecularIor' : [1.5,1.5,1.5], 
	'color roughSpecularExtinctionCoeff' : [0.0,0.0,0.0], 
	'float roughSpecularRoughness' : [0.5], 
})
ri.Cylinder (0.7,-0.9,0.9,360)
ri.TransformEnd()
ri.TransformEnd()
################################################################################

################################################################################
ri.AttributeBegin()
#ri.Attribute( 'identifier',{ 'name' :'table'})
ri.Bxdf('PxrDiffuse', 'wood', 
{ 
    'color diffuseColor' : [0.8,0.8,0.8]
})
ri.Patch('bilinear', {ri.P: [-9, -3, -2, -9, 3, -2, 9, -3, -2, 9, 3, -2]})
ri.AttributeEnd()
################################################################################


# end our world
ri.WorldEnd()
# and finally end the rib file
ri.End()
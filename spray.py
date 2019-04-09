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
ri.Format(1920,1080,1)

# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE)

# now we start our world
ri.WorldBegin()
ri.Rotate(-90,1,0,0)
ri.Translate(0,-7,-1)

#BaseBottom
ri.Cylinder (1.2,-2,2,360)

ri.TransformBegin
#BaseTop
ri.Translate(0,0,2)
ri.Sphere (1.2,0,0.95,360)
ri.TransformBegin
#Cap
ri.Translate(0,0,1.93)
ri.Cylinder (0.7,-0.9,0.9,360)
ri.TransformEnd
ri.TransformEnd

# end our world
# ri.ArchiveRecord(ri.COMMENT, 'end our world')
ri.WorldEnd()

# and finally end the rib file
ri.End()
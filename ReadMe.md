# GPUTrace Utilities

Tools to extract SceneKit shader data from a Metal GPU trace and add them to a Swift Playground.

Apple does not make it easy to export all of the data since the export function only exports the first buffer.

In addition Xcode does not let you export the vertex attributes...

## Getting Started

<sup>*The following assumes you are in the project's root directory.</sup>

Make a copy of the GPUTrace.playground, let's call it `Trace1.playground`

Export the FrameContant0 from a SceneKit Metal GPU trace buffer state.

From the terminal run:

```
cat FrameConstant0 | ./extractFrameContants.py >> Trace1.playground
```

Next double click on the FrameConstant0 attribute denoted by [scn_node] in the debugger.

Copy and paste the row you are interested in into a new file, let's call it `NodeConstants.tsv`

Then from the terminal run:

```
cat NodeConstants.tsv | ./extractFrameAttributes.py >> Trace1.playground
```

Next double click on the vertex attribute buffer in the debugger.

Copy and paste the vertices you are interested in into a new file, let's call it `Vertices.tsv`

Then from the terminal run:

```
cat Vertices.tsv | ./extractFrameAttributes.py >> Trace1.playground
```



## Start playing!


import React from "react";
import { Niivue, NVImage } from "@niivue/niivue";
import { NiivuePanel } from "./components/NiivuePanel.jsx";
import Layer from "./components/Layer.jsx";

let nv = new Niivue({
  loadingText: "drag and drop image...",
});

export default function Doc3d(props) {
  const [layers, setLayers] = React.useState(nv.volumes);

  React.useEffect(async () => {
    // props.volumes.map(async (vol)=>{
    //   let image = await NVImage.loadFromUrl({url:vol.url})
    //   nv.addVolume(image)
    //   setLayers([...nv.volumes])
    // })
    await nv.loadVolumes(props.volumes);
    setLayers([...nv.volumes]);
  }, []);

  nv.opts.onImageLoaded = () => {
    setLayers([...nv.volumes]);
  };

  const layerList = layers.map((layer) => {
    return (
      <Layer
        key={layer.name}
        image={layer}
        onColorMapChange={nvUpdateColorMap}
        onRemoveLayer={nvRemoveLayer}
        colorMapValues={nv.colormapFromKey(layer.colorMap)}
        getColorMapValues={(colorMapName) => {
          return nv.colormapFromKey(colorMapName);
        }}
      />
    );
  });

  function runAI() {
    // let buttonElem = document.getElementById("runAI");
    console.log("clicked. sent to fastapi");
  }

  const buttonStyle = {
    height: "20px",
    display: "flex",
  };

  return (
    <>
      <NiivuePanel nv={nv} volumes={layers}></NiivuePanel>
      <button style={buttonStyle} id="runAI" onClick={() => runAI()}>
        Run AI
      </button>
    </>
  );
}

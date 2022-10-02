<script>
  let fileInput
  let files
  let info

  const postImgOptions = {
    method: 'POST',
    headers: {
      'Accept': '*',
    },
    body: info
  };

  function processImg(img) {
    info = img
    console.log("image from process img", info)
    uploadImage(img)
  }

  async function uploadImage(img) {
    console.log("img from upload function", img)

    try {
      const response = await fetch("http://localhost:8000/upload", postImgOptions);
      if (!response.ok) {
        throw new Error(`Error! Status: ${response.status}`)
      }

      console.log(response.headers)

      const result = await response.blob();
      return result;
    } catch (err) {
      console.log(err)
      return err
    }
  }
</script>

<div class="container">
  {#if info}
    <h2>{info.name}</h2>
  {:else}
    <h2>nothing yet</h2>
  {/if}
  <input class="hidden" id="file-to-upload" type="file" accept="*" bind:files bind:this={fileInput} on:change={() => processImg(files[0])}/>
  <button class="upload-btn" on:click={() => fileInput.click()}>Upload</button>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .hidden {
    display: none;
  }

  .upload-btn {
    width: 128px;
    height: 32px;
    background-color: black;
    font-family: sans-serif;
    color: white;
    font-weight: bold;
    border: none;
  }

  .upload-btn:hover {
    background-color: white;
    color: black;
    outline: black solid 2px;
  }
</style>

<script>
  import _ from 'lodash'

  let  avatar, fileinput, promise = {};

	const onFileSelected = (e) => {
    let image = e.target.files[0];
    let reader = new FileReader();

    reader.readAsDataURL(image);
    reader.onload = (e) => {
      avatar = e.target.result
    };

    uploadFunction(image)
  }

  async function uploadFunction(img) {
    const FD = new FormData()
    FD.append('file', img)

    // for (const [name, value] of Object.entries(img)) {
    //   FD.append(name, value)
    // }

    const response = await fetch('http://localhost:8000/upload', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
      },
      body: FD
    });

    const result = await response.json();
    promise = result
    return result
  }
  
</script>

<div id="app">
  <h1>Upload Image</h1>

  {#if avatar}
  <img class="avatar" src="{avatar}" alt="d" />
  {:else}
  <img class="avatar" src="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png" alt="" /> 
  {/if}
  <img class="upload" src="https://static.thenounproject.com/png/625182-200.png" alt="" on:click={()=>{fileinput.click();}} />
  <div class="chan" on:click={()=>{fileinput.click();}}>Choose Image</div>
  <input style="display:none" type="file" accept=".jpg, .jpeg, .png" on:change={(e)=>onFileSelected(e)} bind:this={fileinput} >

</div>

{#if _.isEmpty(promise)}
	<h2>Loading....</h2>
{:else}
	<h2>{promise.message}</h2>
{/if}

<style>
  #app{
    display:flex;
		align-items:center;
		justify-content:center;
		flex-flow:column;
  }
  .upload{
		display:flex;
    height:50px;
		width:50px;
		cursor:pointer;
	}
	.avatar{
		display:flex;
		height:200px;
		width:200px;
	}
</style>

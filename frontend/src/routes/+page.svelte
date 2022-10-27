<script>
  import SubmitImg from "../components/submitImg.svelte";

  const fetchImage = (async () => {
    // const response = await fetch('https://dog.ceo/api/breeds/image/random')
    const response = await fetch('http://localhost:8000/infer')
    return await response.json()
	})()

</script>
<h1 class="text-3xl font-bold">Welcome to SvelteKit</h1>
<SubmitImg />

{#await fetchImage}
	<p>...waiting</p>
{:then data}
	<img src="pred_slice_3.png" alt="Dog image" />
	<img src="pred_slice_5.png" alt="Dog image" />
	<img src="pred_slice_7.png" alt="Dog image" />
	<img src="pred_slice_9.png" alt="Dog image" />
	<img src="pred_slice_10.png" alt="Dog image" />
	<img src="pred_slice_12.png" alt="Dog image" />
  <!-- <p>{data[0].filename}</p> -->
  <p>{data[0].path}</p>
{:catch error}
	<p>An error occurred: {error}</p>
{/await}

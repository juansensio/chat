<script>
  let prompt = "";
  let prompts = [];
  let responses = [];
  let loading = false;
  const generate = () => {
    if (!prompt || prompt.length == 0) return;
    prompts = [...prompts, prompt];
    responses = [...responses, "Loading..."];
    loading = true;
    fetch("http://localhost:8000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    })
      .then((res) => res.json())
      .then((res) => {
        responses = [...responses.slice(0, -1), res.response];
        loading = false;
      })
      .catch((err) => {
        alert(err.message);
        loading = false;
        responses = [...responses.slice(0, -1), "Failed :("];
      });
    prompt = "";
  };
</script>

<main class="p-3 flex flex-col w-full h-screen justify-between">
  <div>
    <h1 class="text-3xl font-bold">ChatGPT clone</h1>
    <div class="overflow-auto">
      {#each prompts as prompt, i}
        <div class="p-2 rounded-lg">{prompt}</div>
        <div class="bg-gray-200 p-2 rounded-lg">{responses[i]}</div>
      {/each}
    </div>
  </div>
  <form on:submit|preventDefault={generate} class="flex flex-row gap-3">
    <input
      type="text"
      class="border border-2-gray p-2 w-full"
      placeholder="Prompt..."
      bind:value={prompt}
    />
    <button
      disabled={loading}
      type="submit"
      class="border border-2-gray p-2 {loading ? 'bg-gray-200' : ''}}"
      >Generate</button
    >
  </form>
</main>

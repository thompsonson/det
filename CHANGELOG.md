# CHANGELOG





## v0.5.0 (2024-09-27)

### Chore

* chore(release): bump version to v0.4.2 ([`2bad3e7`](https://github.com/thompsonson/det/commit/2bad3e7826dd3499f49f0722e6347b3494414e8c))

* chore(release): bump version to v0.4.2 ([`317fd51`](https://github.com/thompsonson/det/commit/317fd51f21484050f09c42ac4fb4b408cfa45349))

* chore: remove OPENAI_API_KEY from the tests ([`5f57035`](https://github.com/thompsonson/det/commit/5f57035ad8d15fc6f600240044f4a4f6c6e0765b))

* chore: remove OPENAI_API_KEY from the tests ([`280e44e`](https://github.com/thompsonson/det/commit/280e44e47c3bf833129320637a2c9c5b7738a570))

### Ci

* ci: fgracefully handle no package to publish ([`dc6d7f9`](https://github.com/thompsonson/det/commit/dc6d7f946f906ea9aaf05dd959d59976029a7e72))

### Documentation

* docs: updated the installation instructions ([`e260e8e`](https://github.com/thompsonson/det/commit/e260e8e87099db0d6ad9baae053cfa347cdea326))

### Feature

* feat: Groq as LLM provider ([`69ef2ec`](https://github.com/thompsonson/det/commit/69ef2ecf0bd945758043808c50cb701b37ec8ded))

### Unknown

* ran ruff format and check ([`9cf6d27`](https://github.com/thompsonson/det/commit/9cf6d273d7deff88eca9460bd9c5f04ea5bfacb0))

* Merge branch &#39;main&#39; into groq_integration ([`95f3334`](https://github.com/thompsonson/det/commit/95f333428916b01cb2e731f4ff7bd6d0d0b88235))

* formatting and embeddings error handling ([`59bfcdc`](https://github.com/thompsonson/det/commit/59bfcdc18429e97cfda1d02a164542eda42f81d3))

* changed the error handling logic ([`d859d9e`](https://github.com/thompsonson/det/commit/d859d9e4be5928180f401991552366936403c05f))

* adding groq api key setup documentation ([`aa8f6c6`](https://github.com/thompsonson/det/commit/aa8f6c6007b0bc34dd192465828b560467295c34))

* ### Feat
* Feat: Groq LLM provider added
* Feat: API_key validation for `Openai` and `Groq` added ([`b31be9d`](https://github.com/thompsonson/det/commit/b31be9d6b79312549e8048e5697b71a93a02e3e0))

## v0.4.1 (2024-09-25)

### Fix

* fix: caching logic (#22)

* fixing caching logic

* removing print statements

* running ruff format

* formatting as it was previously

---------

Co-authored-by: someshfengde &lt;somesh@culinda.com&gt; ([`b904200`](https://github.com/thompsonson/det/commit/b904200f36f2b4c4eed5a56069451d8094289161))

## v0.4.0 (2024-09-18)

### Chore

* chore: additional tests for the embeddings and langchain

additional tests for the embeddings and langchain ([`2bd89df`](https://github.com/thompsonson/det/commit/2bd89dfcf4895fc4445bdb1bd072b941b26ffb10))

* chore: remove unused import from test_llm_langchain.py ([`e478ea9`](https://github.com/thompsonson/det/commit/e478ea9d3b8fdaaf2128a7624c7278d035e72aa0))

### Ci

* ci: debuging the environment ([`a58ecd6`](https://github.com/thompsonson/det/commit/a58ecd692eb09ae421f3f4430e59e3acb7280497))

* ci: debuging the environment ([`296178b`](https://github.com/thompsonson/det/commit/296178b7b2e1c6561f21a91cf8833bae6e94a090))

* ci: debuging the environment ([`df36a4a`](https://github.com/thompsonson/det/commit/df36a4a487c1fa4303250e3fbb1ded694039b48e))

* ci: debuging the environment ([`d5d33ae`](https://github.com/thompsonson/det/commit/d5d33ae4cf5373461d2e84cbcdc3623b164730cc))

* ci: debuging the environment ([`16fe833`](https://github.com/thompsonson/det/commit/16fe833a21a4185d40927ccaf84c71f170b73155))

### Feature

* feat: create cache file if it does not exist and initialize with an empty dictionary ([`41afb37`](https://github.com/thompsonson/det/commit/41afb3734f03debe70ce9cc54c03a14d7367fd18))

### Fix

* fix: configured the pipeline to use dummy keys ([`0ab78a5`](https://github.com/thompsonson/det/commit/0ab78a5d581cbab62a1567141b4d17a7f53ee4c9))

* fix: configured the pipeline to use dummy keys ([`d89b3a4`](https://github.com/thompsonson/det/commit/d89b3a44fa362013ad2ca447a0e96558425d7401))

* fix: formatting ([`9d33d0a`](https://github.com/thompsonson/det/commit/9d33d0a123a69e1a20df7b4629d70859e1cd440e))

* fix: create cache file if it doesn&#39;t exist in OpenAIEmbeddingGeneratorAdapter initialization ([`f473410`](https://github.com/thompsonson/det/commit/f47341079696746adb2cb1a91705bf102a67ef18))

* fix: create cache file if it doesn&#39;t exist on adapter initialization ([`6bdddfd`](https://github.com/thompsonson/det/commit/6bdddfd6d67e38364f7c8c248cbcd0a406a9c8ab))

* fix: handle empty or unpicklable cache file in EmbeddingsCache to prevent TypeError ([`fb81fc8`](https://github.com/thompsonson/det/commit/fb81fc8c7d1d009a34042d9e86b74638a6f301bd))

* fix: update resources_dir fixture to point to the correct resources directory ([`f6b7a8d`](https://github.com/thompsonson/det/commit/f6b7a8d715b6ff0dc490b8f7c7a9bf0d2a24d189))

* fix: Improve cache loading logic to avoid unnecessary file creation and ensure valid initialization of the cache. ([`a8dd5b0`](https://github.com/thompsonson/det/commit/a8dd5b0c20506ff21ae7a49ea1bab7190e203152))

### Test

* test: Fix mocking of chain&#39;s invoke method in llm_langchain tests to resolve ValueError ([`fd740dd`](https://github.com/thompsonson/det/commit/fd740dd6885aed0a8603d7f918df99713005d796))

* test: Add unit tests for LangChainClient response generation and fix undefined OutputParserException import ([`8be8d73`](https://github.com/thompsonson/det/commit/8be8d73f0e6ae88d3b59caa22cd6038bd021a645))

* test: Add response generation tests for LangChainClient including success, unconfigured chain, and retry mechanism scenarios ([`f088e2c`](https://github.com/thompsonson/det/commit/f088e2c359d8d5706daad7661493213aaca87345))

* test: Add tests for configure_chain method and fix undefined ChatPromptTemplate import ([`bcbe771`](https://github.com/thompsonson/det/commit/bcbe771c0a81a65e75ec1608d6ce5bef76ddb47d))

* test: Add unit tests for chain configuration handling in LangChainClient ([`f838dd1`](https://github.com/thompsonson/det/commit/f838dd1eab358e09a5ca2ecdd4edb0c5679b3b3a))

* test: Add unit tests for LangChainClient&#39;s configure_chain method and fix undefined PromptManager import ([`15c0897`](https://github.com/thompsonson/det/commit/15c0897b9f7585ca69b7b027e2d110d301d84ce1))

* test: add unit tests for chain configuration in LangChainClient ([`a960138`](https://github.com/thompsonson/det/commit/a9601381436b9752d66f70c3eec50f4f62092b31))

* test: Fix LangChainClient initialization test by providing correct prompts file path and adding resources directory fixture ([`1d44696`](https://github.com/thompsonson/det/commit/1d446969af6f44b4ef96bc6fccabecbce342878e))

* test: add initialization test for LangChainClient class ([`34babda`](https://github.com/thompsonson/det/commit/34babdac12db7f119099ac065cff8056e058c4a1))

* test: add test for handling an existing but empty cache file in OpenAIEmbeddingGeneratorAdapter ([`7d7f18c`](https://github.com/thompsonson/det/commit/7d7f18c206d6b38cd8afb3561c9715b3b5646f6b))

* test: add test for cache creation on new adapter instance ([`450d7b3`](https://github.com/thompsonson/det/commit/450d7b3353d7ae92c58e2a7c6239ac8a4ea98eda))

### Unknown

* &#34;fix: manual update to aider generated tests - removed deep LangChain chain tests&#34; ([`28ee07b`](https://github.com/thompsonson/det/commit/28ee07bd017c62ab2c1795fad769b4f6efa16459))

* &#34;fix: test_cache_creation_on_new_adapter_instance&#34; ([`32f944a`](https://github.com/thompsonson/det/commit/32f944a7a7bcb2ccc2befc58482c4e8b79ce77b6))

## v0.3.2 (2024-09-17)

### Fix

* fix: removed the incorrect version in the README ([`7230dc8`](https://github.com/thompsonson/det/commit/7230dc8ce0085b0e4cfc47f289f93ec7e53faaad))

## v0.3.1 (2024-09-17)

### Fix

* fix: corrected the image locations for the check_chain readme ([`6d47b34`](https://github.com/thompsonson/det/commit/6d47b349dbaa8cc8ce7577179602474b61e49063))

## v0.3.0 (2024-09-17)

### Chore

* chore: remove unneeded presentation code and added help documentation to the commands. ([`a511196`](https://github.com/thompsonson/det/commit/a511196ae624dd7f7478b32ba9840ffaa920a9b4))

### Feature

* feat: LangChain Structured Output consistency analysis ([`254d354`](https://github.com/thompsonson/det/commit/254d3540b09be6e9e82c3284a6679ba741400136))

### Fix

* fix: documentation for LangChain Structured Output Chains ([`594c362`](https://github.com/thompsonson/det/commit/594c362e2b8baf25a26bda4a4f6ccb16a643cd97))

* fix: readable layout of example commands ([`1c2e108`](https://github.com/thompsonson/det/commit/1c2e1089ee9f30e1616acb908056b3d8b16451d5))

* fix: readable layout of example commands ([`9483166`](https://github.com/thompsonson/det/commit/9483166ce3986b988af30c39a26966ce58206b2b))

### Unknown

* Merge pull request #20 from thompsonson/LangChain

LangChain Structured Output Chains ([`0457a09`](https://github.com/thompsonson/det/commit/0457a0945aad2be0d2d166d25c1999fd98050e90))

* stash: naughty stash of code developed for H&amp;B but not documented (naughtygit) ([`2931d03`](https://github.com/thompsonson/det/commit/2931d03f57713a09d52813ef0417172531b6e13e))

## v0.2.1 (2024-03-01)

### Fix

* fix: publishing from poetry (rather than semantic-release)

fix: publishing from poetry (rather than semantic-release) ([`f5a6f96`](https://github.com/thompsonson/det/commit/f5a6f96b29d266211aabbadc7672c2b5bf582a8c))

* fix: publishing from poetry (rather than semantic-release) ([`5ac6e7c`](https://github.com/thompsonson/det/commit/5ac6e7ce0caa8db60eee725c2efbc9318f21d835))

## v0.2.0 (2024-03-01)

### Ci

* ci: Ignore errors from files already existing in the repository.

ci: Ignore errors from files already existing in the repository. ([`dc207de`](https://github.com/thompsonson/det/commit/dc207de05a4018c7649646de7c43062754b4ddef))

* ci: Ignore errors from files already existing in the repository. ([`e33f664`](https://github.com/thompsonson/det/commit/e33f664ae3beee10a3e71c60cff3ad5c9c81bb0f))

* ci: updating workflow

ci: updating workflow ([`5fbbb1f`](https://github.com/thompsonson/det/commit/5fbbb1fc86398286d8be101dc8697b56d6a7d224))

* ci: updating workflow ([`21299c2`](https://github.com/thompsonson/det/commit/21299c20da6f280026291a174ec9f22082abbdfb))

### Feature

* feat(publish): automagic publishing of the python package

feat(publish): automagic publishing of the python package ([`a240b26`](https://github.com/thompsonson/det/commit/a240b263a729722d3ba5cdf01d958869cad5b1ec))

* feat(publish): automagic publishing of the python package ([`0747d8c`](https://github.com/thompsonson/det/commit/0747d8c27ff81bd154646926c6e6fe6c78a09e06))

### Fix

* fix: patch to give write permissions to the Action

fix: patch to give write permissions to the Action ([`da465dc`](https://github.com/thompsonson/det/commit/da465dcb6172c5b31dc0b68bc8de9c8da82c139f))

* fix: patch to give write permissions to the Action ([`0b3ab06`](https://github.com/thompsonson/det/commit/0b3ab069186dcc41594da3a190a5cf0d8790aa3e))

* fix: patch update to trigger version 0.2.1

fix: patch update to trigger version 0.2.1 ([`1f07b09`](https://github.com/thompsonson/det/commit/1f07b0943f0cd5a1400828f4fe5e14ede5441ccc))

* fix: patch update to trigger version 0.2.1 ([`2d064e6`](https://github.com/thompsonson/det/commit/2d064e6bb23b7f9612ac5962bc9b23b12af9ae19))

* fix(changelog): correcting the template

fix(changelog): correcting the template ([`7a0d9e0`](https://github.com/thompsonson/det/commit/7a0d9e044f710bfe7ea5384dcd46250ac6de34de))

* fix(changelog): correcting the template ([`0597e4e`](https://github.com/thompsonson/det/commit/0597e4e2f43e2728a8808e748c52b3e2cccd683b))

* fix: adding the GH token and setting the build command to not reinstall poetry

fix: adding the GH token and setting the build command to not reinsta… ([`52a8428`](https://github.com/thompsonson/det/commit/52a842823ad2371be0d50eb1961444ef03aa94c4))

* fix: adding the GH token and setting the build command to not reinstall poetry ([`8ff869e`](https://github.com/thompsonson/det/commit/8ff869ecc53b22624767719df2b34756dce02f48))

* fix: adding the PyPi token to poetry config

fix: adding the PyPi token to poetry config ([`8830ab6`](https://github.com/thompsonson/det/commit/8830ab69b896242f0d5de002b20558bcf7b7598f))

* fix: adding the PyPi token to poetry config ([`d589ab9`](https://github.com/thompsonson/det/commit/d589ab90d796fa429152e308442bc49eef60fddb))

* fix: correcting config for python-semantic-release to work with poetry

fix: correcting config for python-semantic-release to work with poetry ([`c0a3282`](https://github.com/thompsonson/det/commit/c0a3282d5d981c08a40135e20f2fdc9c6d3195f5))

* fix: correcting config for python-semantic-release to work with poetry ([`362ccd9`](https://github.com/thompsonson/det/commit/362ccd999bf8a4427b1807c6d73b121664003460))

### Unknown

* doc: What&#39;s Changed section in the CHANGELOG.md ([`f151beb`](https://github.com/thompsonson/det/commit/f151beb4ed6135168b69e091f36fc4f8a82967df))

* doc: What&#39;s Changed section in the CHANGELOG.md ([`f549190`](https://github.com/thompsonson/det/commit/f549190f302b5dfc7407ae164924f845326ea286))

## v0.1.0 (2024-03-01)

### Ci

* ci: configured to allow running the ci_cd workflow manually ([`ef9fd38`](https://github.com/thompsonson/det/commit/ef9fd38ad2bfc7e4c44595db56903b65ed107162))

* ci: adding codium PR agent ([`be8e010`](https://github.com/thompsonson/det/commit/be8e010a272ab6da260b4003c195ec1e66d5b18e))

* ci: Formatting and Style checks for the pipeline ([`12e6de6`](https://github.com/thompsonson/det/commit/12e6de6c265385f13941674ac7cb7d3a26a14ade))

* ci: Poetry based environments on the ci-cid pipeline ([`33ac693`](https://github.com/thompsonson/det/commit/33ac693edf28e7ca46d1465a0f461bfdabb35385))

### Documentation

* docs: Displays the CI/CD status on the readme. ([`ea9a939`](https://github.com/thompsonson/det/commit/ea9a939d8701fde1d51b237c5cdab9a2f00f5ed6))

* docs: Getting started instructions and notes on development added ([`3350976`](https://github.com/thompsonson/det/commit/33509763e36ce49b7f94101a7b94cb4591caeafa))

### Feature

* feat(llm): Ollama as an LLM Provider 🚀 💨 🦙 

Test the consistency of your local LLMs !

Tested with Mistral 💨 and Llama2 🦙 ([`e4492dd`](https://github.com/thompsonson/det/commit/e4492dd961cad2282b7598f3f4041d7447d79358))

* feat(llm): Use Ollama as the LLM Provider ([`532610d`](https://github.com/thompsonson/det/commit/532610d5c03015c6708343e6555e8b0009bb61d2))

* feat: analyse differences and semantic similarity of the responses to a prompt. Works only with OpenAI presently. ([`d1ca875`](https://github.com/thompsonson/det/commit/d1ca8752b14d4db0a5bba754e1a14863672a8c01))

### Fix

* fix: pyproject config for sementic-release

fix: pyproject config for sementic-release ([`79e81fe`](https://github.com/thompsonson/det/commit/79e81fe295eca61ceca1511e32c765a05281b07d))

* fix: pyproject config for sementic-release ([`87c10e4`](https://github.com/thompsonson/det/commit/87c10e49c3827366bf621d4c5c4ad2be1bd31dc2))

* fix: specific the main branch for sementic-release ([`c6b04fb`](https://github.com/thompsonson/det/commit/c6b04fb9623d0e90cb31202394d13e6fe1966051))

* fix: automatic versioning and package publishing

fix: automatic versioning and package publishing ([`a1df0d5`](https://github.com/thompsonson/det/commit/a1df0d5cc0ba0f60d2b0458ca796bad946848246))

* fix: automatic versioning and package publishing ([`9f465ca`](https://github.com/thompsonson/det/commit/9f465ca8199f71d92775ce107d814996b0dcb5e3))

* fix(openai): handle no api_key gracefully ([`333a3ef`](https://github.com/thompsonson/det/commit/333a3efe2b77462f5743c576261b645cea59cefb))

### Refactor

* refactor(embeddings): optimize embedding cache handling and embedding test fixtures

refactor(embeddings): optimize cache handling and test fixtures ([`6a539bb`](https://github.com/thompsonson/det/commit/6a539bbe75e5afed0e37dbb66ccb6cc30c347220))

* refactor(embeddings): optimize cache handling and test fixtures ([`07ae70b`](https://github.com/thompsonson/det/commit/07ae70b8c9663403d11f910db5afbcf1dae3c617))

* refactor: tests for the helplers ([`219b9c7`](https://github.com/thompsonson/det/commit/219b9c781684426a997e25817aec6ab7efe8cfff))

* refactor: tests for the helplers ([`3787883`](https://github.com/thompsonson/det/commit/37878839117ce34d957526047a69a1d3279b284b))

### Unknown

* 0.1.3 ([`aa38451`](https://github.com/thompsonson/det/commit/aa38451d151a2eb6188fc2741d182ddfc03f386c))

* Fix: Python package publishing from CI/CD

Fix: Python package publishing from CI/CD ([`f986f05`](https://github.com/thompsonson/det/commit/f986f0585c34436b3ddf0660394aebcc34443ec2))

* Establishing Github Actions for style, format, and tests

Establishing Github Actions for style, format, and tests ([`8d54cec`](https://github.com/thompsonson/det/commit/8d54cec364bdb8f939033a2b9ed4dde0980a0fd5))

* Initial commit ([`f7126a4`](https://github.com/thompsonson/det/commit/f7126a424ec7cab51d1fd8e91446c10d2f633965))

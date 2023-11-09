# Readme for Stage Builder
25 Oct 2023 - Mike Wise

## Installing Dependencies:

### Colored
   ```
   $: pip install colored
   ```

### USD

```
$: git clone https://github.com/PixarAnimationStudios/OpenUSD
```

Open a developer console

```
$: python OpenUSD\build_scripts\build_usd.py "C:\USD"
```

## To run:

   ```
   $: python buildstage.py -c BaeDefs.json -s DroneDesign -of out.usda -a a -r Admin
   ```

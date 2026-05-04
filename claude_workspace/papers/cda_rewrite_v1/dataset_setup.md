# DomainBed Dataset Setup for CDA

This records how the non-PACS datasets should be installed on the HPC for the CDA runs.

## Root

Use the existing `domaingen` data root:

```text
/project/jje239_dgxpublicai25/jwje228/work/domaingen/data
```

The code expects:

```text
domaingen/data
+-- PACS
+-- VLCS
+-- office_home
+-- terra_incognita
+-- domain_net
```

## Downloader

Use:

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
python -m domaingen.download_data \
  --dataset remaining \
  --data_dir /project/jje239_dgxpublicai25/jwje228/work/domaingen/data
```

`remaining` means:

- `VLCS`
- `OfficeHome`
- `TerraIncognita`
- `DomainNet`

## Replacement Links

The old DomainBed links for `VLCS` and `OfficeHome` are stale. `domaingen.download_data` uses these replacement Google Drive IDs:

- `VLCS`: `1yDuLrJdPSvMbTmpq-7XmwG0HnJengD-T`
- `OfficeHome`: `1USXqK4nCvOAR5Ty4iwKcuCOrRJoRuDyU`

## DomainNet Duplicates

DomainNet uses the official DomainBed duplicate list:

```text
domaingen/misc/domain_net_duplicates.txt
```

After extracting DomainNet, the downloader removes those duplicate files and writes:

```text
domaingen/data/domain_net/.domainbed_duplicates_removed
```

## Verification

After download, run:

```bash
python -m domaingen.download_data \
  --dataset all \
  --data_dir /project/jje239_dgxpublicai25/jwje228/work/domaingen/data \
  --verify_only
```

Expected folder names:

- `VLCS`: `Caltech101`, `LabelMe`, `SUN09`, `VOC2007`
- `OfficeHome`: `Art`, `Clipart`, `Product`, `Real World`
- `TerraIncognita`: `location_100`, `location_38`, `location_43`, `location_46`
- `DomainNet`: `clipart`, `infograph`, `painting`, `quickdraw`, `real`, `sketch`

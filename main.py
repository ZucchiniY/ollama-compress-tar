import json
import pandas as pd
import os
import tarfile


def tar_ollama_model(main_path, tar_path, model_name, model_version):
    json_path = os.path.join(main_path, 'manifests/registry.ollama.ai/library/', model_name, model_version)
    blob_path = os.path.join(main_path, 'blobs/')

    with open(json_path) as f:
        df = json.load(f)

    out = pd.json_normalize(df, record_path=['layers'], meta=['schemaVersion', 'mediaType', 'config'],
                            meta_prefix='layer_')

    config = out.layer_config[0]['digest']
    results = list(map(lambda x: x.replace(':', '-'), out.digest.values))
    results.append(config)

    files = list(map(lambda x: os.path.join(blob_path, x), results))
    files.append(json_path)

    out_file_tar_name = os.path.join(tar_path, model_name + ".tar.gz")
    with tarfile.open(out_file_tar_name, "w:gz") as tar:
        for file in files:
            tar.add(file)

    print(f"{model_name}:{model_version} 打包完成，保存在 {out_file_tar_name}")


if __name__ == '__main__':
    main_path = "$OLLAMA_MODELS"
    tar_path = "$ARCHIVE_PATH"
    model_name = "gemma2"
    model_version = "latest"
    tar_ollama_model(main_path,tar_path, model_name, model_version)

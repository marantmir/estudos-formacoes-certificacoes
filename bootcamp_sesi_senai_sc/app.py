"""
Streamlit front-end para o projeto de Manutenção Preditiva do Bootcamp.
- Upload de Bootcamp_train.csv (obrigatório) e Bootcamp_test.csv (opcional)
- Detecção / mapeamento das colunas de falha (interface para confirmar)
- Pré-processamento, comparação de modelos e geração de submissão
"""
import streamlit as st
import pandas as pd
import traceback, sys

from utils import carregar_e_processar_dados, detect_failure_columns, preprocess_pipeline
from modelos import comparar_e_treinar_modelos, gerar_predicoes_para_submissao

st.set_page_config(page_title="🔧 Manutenção Preditiva", page_icon="🔧", layout="wide")
st.title("🔧 Sistema Inteligente de Manutenção Preditiva")

st.markdown("""
Carregue:
- **Bootcamp_train.csv** (obrigatório) — contém rótulos.
- **Bootcamp_test.csv** (opcional) — sem rótulos; será usado para gerar `predicoes_submission.csv`.
""")

arquivo_treino = st.file_uploader("📂 Selecione Bootcamp_train.csv", type=["csv"])
arquivo_teste = st.file_uploader("📂 Selecione Bootcamp_test.csv (opcional)", type=["csv"])

if arquivo_treino:
    try:
        treino_df = carregar_e_processar_dados(arquivo_treino)
        teste_df = carregar_e_processar_dados(arquivo_teste) if arquivo_teste else None

        st.success("✅ Arquivo de treino carregado.")
        st.write("Preview (treino):")
        st.dataframe(treino_df.head())

        st.markdown("### 1) Detecção automática das colunas de falha")
        detection = detect_failure_columns(treino_df)
        st.write("Mapeamento automático (aliases):")
        st.json(detection["detected_map"])
        st.write("Colunas 0/1 candidatas:", detection["candidate_binary_cols"])

        st.markdown("### 2) Confirme/ajuste o mapeamento (se necessário)")
        canonical = ["fdf", "fdc", "fp", "fte", "fa"]
        cols_options = [""] + detection["all_columns"]
        user_map = {}
        for can in canonical:
            default = detection["detected_map"].get(can) if detection["detected_map"].get(can) else ""
            idx = cols_options.index(default) if default in cols_options else 0
            user_map[can] = st.selectbox(f"Coluna para {can.upper()}", options=cols_options, index=idx, key=f"map_{can}")

        if st.button("✅ Confirmar mapeamento e executar pipeline"):
            if not all(user_map.values()):
                st.error("Selecione as 5 colunas de falha antes de continuar.")
            else:
                target_columns_actual = [user_map[c] for c in canonical]
                st.info("Rodando pré-processamento (pode levar alguns segundos)...")
                X_train, X_val, y_train, y_val, X_test_proc, preprocess_objects, features, detected = preprocess_pipeline(
                    treino_df, teste_df, target_columns=target_columns_actual, verbose=False
                )

                st.success("Pré-processamento concluído.")
                st.write(f"Features usadas ({len(features)}):")
                st.code(features)

                st.markdown("### 3) Treinamento e comparação de modelos")
                st.info("Treinando e comparando: RandomForest (sempre), LightGBM e XGBoost (se disponíveis).")
                results, best_model = comparar_e_treinar_modelos(X_train, y_train, X_val, y_val)

                # Mostrar resultados
                df_results = pd.DataFrame([{
                    "model_name": r["model_name"],
                    "mean_f1": r["mean_f1"],
                    "hamming_loss": r["hamming_loss"],
                    "subset_acc": r["subset_acc"]
                } for r in results]).sort_values("mean_f1", ascending=False).reset_index(drop=True)

                st.dataframe(df_results)
                st.success(f"Melhor modelo: {results[0]['model_name']} (ver tabela)")

                st.markdown("#### Métricas detalhadas (melhor modelo)")
                best_detail = results[0]
                st.write("Per-label F1 (validação):")
                st.json(best_detail["per_label_f1"])

                # gerar predições para teste se existir
                if X_test_proc is not None:
                    st.markdown("### 4) Gerar predições para submissão")
                    df_pred = gerar_predicoes_para_submissao(
                        best_model,
                        X_test_proc,
                        canonical_targets=preprocess_objects["canonical_targets"],
                        target_map=preprocess_objects["target_columns_actual"],
                        original_test_df=teste_df
                    )
                    st.write("Amostra das predições:")
                    st.dataframe(df_pred.head())
                    csv_bytes = df_pred.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Baixar predicoes_submission.csv", csv_bytes, "predicoes_submission.csv", "text/csv")
                    st.info("Pronto — envie o arquivo à API de avaliação do Bootcamp.")
                else:
                    st.info("Nenhum Bootcamp_test.csv foi fornecido — carregue-o para gerar submissões.")
    except Exception as e:
        tb = traceback.format_exc()
        st.error("❌ Erro no processamento. Veja o traceback abaixo:")
        st.code(tb)
        print(tb, file=sys.stderr)
else:
    st.info("Faça upload do Bootcamp_train.csv para começar.")

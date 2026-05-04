# Literature Style Audit

This audit is generated from downloaded/local TeX sources and is meant to guide the CDA rewrite.

## Validity Caveats Added After Review

- `fad` is not currently valid as writing-style evidence because the extracted source appears to contain rebuttal or fragmentary material rather than stable manuscript prose.
- `wilds` is not currently valid as writing-style evidence because the extracted source has too little usable section prose.
- `diwa` is usable only as partial structural evidence until its PDF or full source is parsed more cleanly.
- Planning files may use `fad`, `wilds`, and `diwa` as topical literature references only after their actual paper claims are checked from PDF or authoritative pages; they should not be used to infer professional prose style from this audit.
- The rewrite must not rely on this audit alone for current coverage. Use `misc/literature_notes/modern_literature_refresh.md` and the literature matrix required in `finalization.md`.

## current_cda
- TeX files scanned: `1`
- Approximate TeX word count: `8783`
- Figures: `8`; tables: `9`; algorithms: `1`
- Section sequence: Introduction, Relationship to prior DG work., Contributions., Related Work and Positioning, Domain generalization and source-only model selection., Weight averaging and post-hoc DG., Robustness, compression, and vector payoffs., A Theoretical Relationship between Distributional Canalization and Domain Generalization, Why diversity only helps directionally., Why averaging needs a deployment bridge., CDA: Post-hoc Domain Generalization by Distributional Canalization, A baseline method: late-window uniform checkpoint averaging, Retained-family selection by version-space compression, Two weighting rules from the same certificate, Soup deployment and mergeability, Empirical analysis of the CDA mechanism, Local flatness analysis., Loss surface visualization.
- Over-explanatory tone hits: {'matters because': 3, 'this is why': 2, 'why ': 8, 'not merely': 2, 'not just': 1, 'does not compete': 1, 'the claim is': 1, 'coherent reason': 1, 'defensible': 1, 'should be read': 2, 'primitive object': 2}

Representative opening paragraphs:
- Domain generalization (DG) methods aim to learn from labeled source domains and generalize to an unseen target domain without using target labels at training or model-selection time \citep{muandet2013domain,li2017deeper,gulrajani2021domainbed}. The setting is common in deployment: an object-recognition system trained on photographs, sketches, and cartoons may be deployed on a new artistic style; a wildlife classifier trained at several camera-trap locations may be deployed at a new location; a product-recognition system trained on curated catalog imagery may be deployed on real user photographs. The common difficulty is that the training dist...
- The recent DG literature changed the standard of evidence for this problem. DomainBed showed that many proposed DG algorithms are not reliably better than carefully tuned empirical risk minimization (ERM) under controlled model selection and hyperparameter protocols \citep{gulrajani2021domainbed}. SWAD then showed that seeking flatter minima through dense, overfit-aware stochastic weight averaging can substantially improve DG performance \citep{cha2021swad}. DiWA and related post-hoc averaging work showed that diversity and weight-space averaging can provide additional deployment-time gains without changing inference cost \citep{rame2022diwa,...
- We study the post-hoc source-only version of DG. The base training run is fixed. It has produced a checkpoint bank \[ \cB=\{\theta_1,\ldots,\theta_K\}, \] and the method may only decide which checkpoints to retain and how to average them. This regime is narrower than training-time DG, but the narrowness is useful because it isolates the deployment question: \begin{quote} \emph{What source-only quantity should govern checkpoint selection and averaging under target-domain shift?} \end{quote} Uniform late-window averaging answers the question implicitly by trusting temporal proximity. SWAD answers it through flatness and overfit-aware averaging....

## swad
- TeX files scanned: `10`
- Approximate TeX word count: `16668`
- Figures: `0`; tables: `2`; algorithms: `1`
- Section sequence: Organization., A baseline method: stochastic weight averaging, Dense and overfit-aware stochastic weight sampling strategy, Empirical analysis of SWAD and flatness, Local flatness anaylsis., Loss surface visualization., Evaluation protocols, Dataset and optimization protocol., Evaluation metrics., Main results, Comparison with domain generalization methods., Ablation study, Exploring the other applications: ImageNet robustness, Potential negative societal impacts, Potential Societal Impacts, Implementation Details, Hyperparameters of SWAD, Hyperparameter search protocol for reproduced results
- Over-explanatory tone hits: {'why ': 3}

Representative opening paragraphs:
- Independent and identically distributed (i.i.d.) condition is the underlying assumption of machine learning experiments. However, this assumption may not hold in real-world scenarios, \ie, the training and the test data distribution may differ significantly by \emph{distribution shifts}. For example, a self-driving car should adapt to adverse weather or day-to-night shifts~\cite{dai2018dark, michaelis2019benchmarking}. Even in a simple image recognition scenario, systems rely on wrong cues for their prediction, \eg, geographic distribution~\cite{de2019does}, demographic statistics~\cite{yang2020towards}, texture~\cite{geirhos2019cnn_biased_to...
- Domain generalization (DG) aims to address \emph{domain shift} simulated by training and evaluating on different domains. DG tasks assume that both task labels and domain labels are accessible. For example, \data{PACS} dataset~\cite{li2017pacs} has seven task labels (\eg, ``dog'', ``horse'') and four domain labels (\eg, ``photo'', ``sketch''). Previous approaches explicitly reduced domain gaps in the latent space~\cite{muandet2013icml_DIFL,ganin2016dann,li2018cdann,bahng2019rebias,zhao2020er_entropy_regularization}, obtained well-transferable model parameters by the meta-learning framework~\cite{li2018mldg,dou2019masf,balaji2018metareg,zhang2...
- Unfortunately, although ERM showed surprising empirical success on DomainBed, simply minimizing the empirical loss on a complex and non-convex loss landscape is typically not sufficient to arrive at a good generalization~\cite{keskar2016largebatch,garipov2018fge,izmailov2018swa,foret2020sharpness}. In particular, the connection between the generalization gap and the flatness of loss landscapes has been actively discussed under the i.i.d. condition~\cite{keskar2016largebatch,dziugaite2017computing,garipov2018fge,izmailov2018swa,jiang2019fantastic,foret2020sharpness}. \citet{izmailov2018swa} argued that seeking flat minima will lead to robustne...

## diwa
- TeX files scanned: `2`
- Approximate TeX word count: `3080`
- Figures: `0`; tables: `0`; algorithms: `0`
- Section sequence: N/A
- Over-explanatory tone hits: {}

Representative opening paragraphs:

## miro
- TeX files scanned: `8`
- Approximate TeX word count: `12726`
- Figures: `1`; tables: `0`; algorithms: `1`
- Section sequence: Introduction, Related works, Domain generalization., Exploiting pre-trained models., Regularization based on mutual information., Methods, Mutual information regularization with oracle, Mutual information analysis with the oracle model, Features and encoders design, Multi-scale features., Design of the mean and variance encoders., Experiments, Evaluation protocols and implementation details, Experiment setups and implementation details, Benchmark datasets., Evaluation protocols and datasets., Implementation details., Implementation details.
- Over-explanatory tone hits: {}

Representative opening paragraphs:
- Emerging studies on the generalizability of deep neural networks have revealed that the existing models, which assume independent and identically distributed (i.i.d.) training and test distribution, are not robust to significant distribution shifts between training and test distribution, \eg, backgrounds \cite{xiao2020background_challenge_bgc}, geographic distribution \cite{de2019does}, demographic statistics \cite{yang2020towards, scimeca2022wcst-ml}, textures \cite{geirhos2019cnn_biased_towards_texture, bahng2019rebias}, or day-to-night shifts \cite{dai2018dark, michaelis2019benchmarking}. Domain generalization (DG) aims to learn robust rep...
- Instead of learning domain-invariant features, we let a model learn similar features to ``oracle'' representations, \ie, an optimal model generalized to \emph{any} domain. In particular, we re-formulate the DG problem by maximizing the mutual information (MI) between the oracle model representations and the target model representations while preserving the training loss on source domains. However, the oracle model is not achievable in practice. Hence, we use a large pre-trained model (\eg, ImageNet pre-trained ResNet-50 \cite{he2016_cvpr_resnet}) as an approximation. With this approximation, we derive a tractable variational lower bound of th...
- While a naive fine-tuning approach of a large pre-trained model can harm the robustness against distribution shifts \cite{wortsman2021robust, kumar2022iclr_finetuning_distort}, our proposed algorithm remarkably improves the robustness against unseen domains during fine-tuning in a plug-and-play manner to any scale of the backbone model and datasets. In our experiment, we observe that the naive fine-tuning of a larger pre-trained model can fail to provide better performances, even though the larger pre-trained model is trained with more data and domains. For example, ERM with the ResNet pre-trained on ImageNet (trained with 1.3M images) shows ...

## qrm
- TeX files scanned: `1`
- Approximate TeX word count: `28863`
- Figures: `6`; tables: `4`; algorithms: `1`
- Section sequence: Introduction, Background: Domain generalization, Quantile Risk Minimization, Algorithms for Quantile Risk Minimization, From QRM to Empirical QRM, Theory: Generalization bound, Theory: Causal recovery, Related work, Experiments, Synthetic datasets, Real-world datasets, DomainBed datasets, Discussion, Conclusion, Causality, Definitions and example, EQRM recovers the causal predictor, Overview.
- Over-explanatory tone hits: {'not just': 1}

Representative opening paragraphs:
- Domain generalization (DG) seeks to improve a system's OOD performance by leveraging datasets from multiple environments or domains at training time, each collected under different experimental conditions~\citep{blanchard2011generalizing, muandet2013domain, gulrajani2020search} (see \cref{fig:fig1:train-test}). The goal is to build a predictor which exploits invariances across the training domains in the hope that these invariances also hold in related but distinct test domains~\citep{gulrajani2020search, schoelkopf2012causal, li2018learning, krueger21rex}. \looseness-1 To realize this goal, DG is commonly formulated as an average-~\citep{bla...
- In this work, we argue that DG is neither an average-case nor a worst-case problem, but rather a probabilistic one. To this end, we propose a probabilistic framework for DG, which we call \textit{Probable Domain Generalization} (\cref{sec:qrm}), wherein the key idea is that distribution shifts seen during training should inform us of \emph{probable} shifts at test time. \looseness-1 To realize this, we explicitly relate training and test domains as draws from the same underlying meta-distribution~(\cref{fig:fig1:q-dist}), and then propose a new optimization problem called \emph{Quantile Risk Minimization} (QRM). By minimizing the $\alpha$-qua...
- To solve QRM in practice, we introduce the \textit{Empirical QRM}~(EQRM) algorithm (\cref{sec:qrm_algs}). Given a predictor's empirical risks on the training domains, EQRM forms an estimated risk distribution using kernel density estimation (KDE, \cite{parzen1962estimation}). Importantly, KDE-smoothing ensures a right tail that extends beyond the largest training risk (see \cref{fig:fig1:risk}), with this risk ``extrapolation''~\citep{krueger21rex} unlocking \emph{invariant prediction} for EQRM (\cref{sec:qrm_algs:eqrm}). We then provide theory for EQRM (\cref{sec:qrm_algs:gen_bound}, \cref{sec:qrm_algs:causality}) and demonstrate empirically...

## domainbed
- TeX files scanned: `1`
- Approximate TeX word count: `15509`
- Figures: `0`; tables: `8`; algorithms: `0`
- Section sequence: Introduction, The problem of domain generalization, Model selection as part of the learning problem, Three model selection methods, Training-domain validation set, Leave-one-domain-out cross-validation, Test-domain validation set (oracle), Considerations from the literature, \domainbed: A PyTorch testbed for domain generalization, Datasets, Algorithms, Implementation choices for realistic evaluation, Large models, Data augmentation, Using all available data, Experiments, Hyperparameter search, Standard error bars
- Over-explanatory tone hits: {'why ': 1}

Representative opening paragraphs:
- Machine learning systems often fail to \emph{generalize out-of-distribution}, crashing in spectacular ways when tested outside the domain of training examples \citep{torralba2011unbiased}. The overreliance of learning systems on the training distribution manifests widely. For instance, self-driving car systems struggle to perform under conditions different to those of training, including variations in light \citep{dai2018dark}, weather \citep{volk2019towards}, and object poses \citep{alcorn2019strike}. As another example, systems trained on medical data collected in one hospital do not generalize to other health centers \citep{castro2019causa...
- Aware of this problem, the research community has spent significant effort during the last decade to develop algorithms able to generalize out-of-distribution. In particular, the literature in \emph{domain generalization} assumes access to multiple datasets during training, each of them containing examples about the same task, but collected under a different domain or environment \citep{blanchard2011generalizing, muandet2013domain}. The goal of domain generalization algorithms is to incorporate the invariances across these training datasets into a classifier, in hopes that such invariances also hold in novel test domains. Different domain gen...
- Despite the enormous importance of domain generalization, the literature is scattered: a plethora of different algorithms appear yearly, and these are evaluated under different datasets and model selection criteria. Borrowing from the success of standard computer vision benchmarks such as ImageNet \citep{russakovsky2015ImageNet}, the purpose of this work is to perform a standardized, rigorous comparison of domain generalization algorithms. In particular, we ask: how useful are domain generalization algorithms in realistic settings? Towards answering this question, we first study model selection criteria for domain generalization methods, resu...

## model_soups
- TeX files scanned: `2`
- Approximate TeX word count: `16881`
- Figures: `10`; tables: `10`; algorithms: `1`
- Section sequence: Notation and preliminaries, An exact expression for logit difference, Derivation of approximation, Detailed empirical evaluations, Evaluation setup., The effect of temperature calibration., Introduction, Method, Experiments, Experimental setup, Intuition and motivation, Model soups, Fine-tuning CLIP and ALIGN, Fine-tuning a ViT-G model pre-trained on JFT-3B, Fine-tuning on text classification tasks, Analytically comparing soups to ensembles, Scope and limitations, Related work
- Over-explanatory tone hits: {}

Representative opening paragraphs:
- We begin by restating and adding to the notation used in Section~\ref{sec:theory}. For a model with parameter vector $\theta\in\R^d$ and input vector $x$, we let $f(x;\theta)\in\R^C$ denote the model's logit output for $C$-way classification. Throughout, we fix two endpoint models $\theta_0$ and $\theta_1$, and for an interpolation parameter $\alpha\in[0,1]$ define \begin{equation*} \theta_\alpha \defeq (1-\alpha) \theta_0 + \alpha \theta_1, ~~\mbox{and}~~ \fwse(x) \defeq f(x; \theta_\alpha) \end{equation*} to be the ``soup'' weight averaged model and its corresponding logits. We also write \begin{equation*} \fose(x) \defeq (1-\alpha)f(x;\the...
- For a logit vector $f\in\R^C$ and a ground-truth label $y$, denote the cross-entropy loss by \begin{equation*} \ell(f;y) = \log\left(\sum_{y'}\exp\{f_{y'}-f_{y}\}\right). \end{equation*} For some distribution over $x,y$ we write the expected $\beta$-calibrated log losses of the soup and ensemble as \begin{equation*} \exloss_\alpha = \E_{x,y} \ell(\beta f(x;\theta_\alpha),y) ~~\mbox{and}~~ \exlossens_\alpha = \E_{x,y} \ell(\beta \fose(x),y), \end{equation*} respectively.
- We have the following expression for the derivatives of cross entropy w.r.t.\ logits. The gradient is \[ \grad_{f}\ell\left(f,y\right)=\softmax(f) - \sbv{y}, \] where $\sbv{i}$ is the $i$th standard basis vector and $\softmax(f)\in\R^C$ has $e^{f_i}/\sum_j e^{f_j}$ in its $i$th entry. The Hessian is \[ \hess_{f}\ell\left(f,y\right)=\mathrm{diag}\left(\softmax\left(f\right)\right) - [\softmax(f)] [\softmax(f)]^T, \] so that for any $v\in \R^C$, we have \begin{equation*} v^T \hess_{f}\ell\left(f,y\right) v = \mathrm{Var}_{Y\sim \softmax(f)} [v_Y]. \end{equation*}

## large_pretraining_dg
- TeX files scanned: `2`
- Approximate TeX word count: `18639`
- Figures: `33`; tables: `23`; algorithms: `1`
- Section sequence: Introduction, Related Work, Analyzing the role of pretraining in Domain Generalization , Testing the Image Similarity Hypothesis, Introducing the Alignment Hypothesis, Re-thinking Domain Generalization Benchmarking using the Alignment Hypothesis  , Data Exploration and Cleaning , Data Splitting, Experiments, Training and Evaluation Protocol, Algorithms, Results, Discussion, Conclusion, Acknowledgments, Appendix, Training and Evaluation Details, Training Compute
- Over-explanatory tone hits: {'why ': 1, 'not just': 1}

Representative opening paragraphs:
- Multi-Source Domain Generalization (DG) is the task of training on multiple source domains and achieving high classification performance on unseen target domains. Recent methods combine robust features from web-scale pretrained backbones with new features learned from source data, and this has dramatically improved benchmark results. However, it remains unclear if DG finetuning methods are becoming better over time, or if improved benchmark performance is simply an artifact of stronger pre-training. Prior studies have shown that perceptual similarity to pre-training data correlates with zero-shot performance, but we find the effect limited in...
- Domain Generalization (DG) addresses the challenge of enabling AI models to generalize from known domains to unseen ones, a critical task given the inevitable distribution shifts between training and real-world deployment~\citep{saenko2010adapting}. DG pipelines typically consist of three stages: pretraining a model on a large, general dataset; finetuning the model with one or more source domains; and finally evaluating the model on target domains that are distinct from source domains. DG methods increasingly rely on huge-scale foundation models for initialization (\eg,~\citep{shu2023clipood,cha2022miro,addepalli2024leveraging}). Simultaneous...
- In this work, we examine the reliance of recent state-of-the-art CLIP-based DG methods on pre-trained features. While prior studies have shown that perceptual similarity to pre-training data explains zero-shot performance—referred to as the Image Similarity Hypothesis~\citep{mayilvahanan2024does}—we find this relationship to be limited in the DG setting. Despite evidence of target domains being present in pre-training (Figure \ref{fig:retrieval}), we find that perceptual similarity alone does not fully explain accuracy in the DG context (Section \ref{sec:analyzing}). We argue that it is not just the presence of similar data in pre-training th...

## dgsam
- TeX files scanned: `2`
- Approximate TeX word count: `20044`
- Figures: `11`; tables: `8`; algorithms: `1`
- Section sequence: Introduction, Preliminaries and Related Work, Domain Generalization, Sharpness-Aware Minimization, Rethinking Sharpness in Domain Generalization, Global Sharpness Pitfalls: The Fake Flat Minima Problem, Analysis of Worst-Case Domain Loss, Methodology, Limitations of Total Gradient Perturbation, Decreased-overhead Gradual SAM (DGSAM), How DGSAM Controls Individual Sharpness, Numerical Experiments, Experimental Settings, Evaluation protocols, Baselines and Datasets, Implementation Details, Accuracy and Domain-wise Variance Across Benchmarks, Variance of Domain-wise Performance, Sharpness Analysis
- Over-explanatory tone hits: {'not merely': 1}

Representative opening paragraphs:
- Deep neural networks achieve remarkable performance under the independent and identically distributed (i.i.d.) assumption \citep{kawaguchi2017generalizationiid}, yet this assumption often fails in practice due to \textit{domain shifts}. For example, in medical imaging, test data may differ in acquisition protocols or device vendors \citep{li2020medical}, and in autonomous driving, variations in weather or camera settings introduce further domain shifts \citep{khosravian2021selfdriving}. Since it is impractical to include every possible scenario in the training data, \emph{domain generalization} (DG) seeks to learn models that generalize to un...
- A common DG strategy is to learn domain-invariant representations by aligning source domain distributions and minimizing their discrepancies \citep{muandet2013moment1, arjovsky2019irm}, adversarial training \citep{li2018adver1, ganin2016dann}, data augmentation \citep{volpi2018generalizing, zhou2020dataaug4, zhou2021dataaug5}, and meta-learning approaches \citep{li2019meta1, balaji2018metareg}. More recently, flat minima in the loss landscape have been linked to improved robustness under distributional shifts \citep{cha2021swad, zhang2022gasam, chaudhari2019entropy}. In particular, Sharpness-Aware Minimization (SAM) \citep{foret2021sam} pertu...
- However, our analysis reveals two fundamental limitations in applying SAM to DG. First, SAM may converge to \textit{fake flat minima}, where the total loss appears flat in terms of global sharpness, but remains sharp when viewed from individual source domains (Section~\ref{subsec:fake_flat_minima}). Second, global sharpness minimization fails to tighten the upper bound on the \emph{average worst-case domain risk}, defined as the maximum expected loss under distribution shifts. In contrast, we show that this upper bound can be expressed in terms of average individual sharpness, indicating that minimizing individual sharpness offers a more reli...

## groupdro
- TeX files scanned: `18`
- Approximate TeX word count: `13369`
- Figures: `7`; tables: `3`; algorithms: `1`
- Section sequence: Algorithm, Discussion, Comparison between group DRO and ERM, Accounting for generalization through group adjustments improves DRO, Results., DRO improves worst-group accuracy under appropriate regularization, $\Ltwo$ penalties., Early stopping., Discussion., ERM and DRO have poor worst-group accuracy in the overparameterized regime, ERM., DRO., Discussion., Experimental details, Datasets, MultiNLI., Waterbirds., CelebA.
- Over-explanatory tone hits: {}

Representative opening paragraphs:
- Overparameterized neural networks can be highly accurate \emph{on average} on an i.i.d.\ test set yet consistently fail on atypical groups of the data (e.g., by learning spurious correlations that hold on average but not in such groups). Distributionally robust optimization (DRO) allows us to learn models that instead minimize the \emph{worst-case} training loss over a set of pre-defined groups. However, we find that naively applying group DRO to overparameterized neural networks fails: these models can perfectly fit the training data, and any model with vanishing average training loss also already has vanishing worst-case training loss. Inst...
- In the convex and batch case, there is a rich literature on distributionally robust optimization which treats the problem as a standard convex conic program \citep{bental2013robust, duchi2016, bertsimas2018data, lam2015quantifying}. For general non-convex DRO problems, two types of stochastic optimization methods have been proposed: (i) stochastic gradient descent (SGD) on the Lagrangian dual of the objective \citep{duchi2018learning,hashimoto2018repeated}, and (ii) direct minimax optimization \citep{namkoong2016stochastic}. The first approach fails for group DRO because the gradient of the dual objective is difficult to estimate in a stochas...
- Recall that we aim to solve the optimization problem \refeqn{htdro}, which can be rewritten as \begin{align} \min_{\theta \in \Theta} \sup_{q \in \Delta_m} \ \sum_{g=1}^m q_g \E_{(x, y) \sim P_g}[\ell(\theta; (x, y))]. \end{align} Extending existing minimax algorithms for DRO \citep{namkoong2016stochastic,oren2019drolm}, we interleave gradient-based updates on $\theta$ and $\padv$. Intuitively, we maintain a distribution $\padv$ over groups, with high masses on high-loss groups, and update on each example proportionally to the mass on its group. Concretely, we interleave SGD on $\theta$ and exponentiated gradient ascent on $\padv$ (\refalg{op...

## eoa
- TeX files scanned: `2`
- Approximate TeX word count: `15425`
- Figures: `4`; tables: `11`; algorithms: `0`
- Section sequence: Appendix, Broader Impact, Training and Evaluation Protocols for DomainBed Benchmarking, Experiments on cross-run rank correlation, Start Iteration, Averaging Frequency, Rank Correlation, Instability Reduction: Qualitative Analysis, Cross-run rank correlation, Why Does Ensembling Improve Performance?, Discussions and Limitations, Cross Run Spearman Correlation, Additional Tables and Plots, Introduction, Model Averaging, Terminology, Model Averaging Protocol, Ablation Analysis
- Over-explanatory tone hits: {'this is why': 1, 'why ': 9}

Representative opening paragraphs:
- We use the training protocol described in \cite{gulrajani2020search} with minor changes: we use a smaller hyper-parameter search space (shown in Table \ref{tab:hyper_param}) and smaller number of random trials for computational reasons, and train on DomainNet dataset for $15,000$ iterations instead of $5,000$ similar to \cite{cha2021swad}, because its training loss is quite high. For a dataset with $D$ domains, we run a total of $6D$ random trials. This results in $6$ experiments per domain, in which this domain is used as the test set, while the remaining domains are used as training/validation set (randomly split). This is also the reason w...
- All models are trained using the ERM objective and optimized using the Adam optimizer \cite{kingma2014adam}. We use ResNet-50 \cite{he2016deep} pre-trained on Imagenet as our initialization for training in all the experiments. In the final benchmarking experiment, we also use ResNeXt-50 32x4d, that is trained using semi-weakly supervised objective on IG-1B targeted (containing 1 billion weakly labeled images) and ImageNet labeled data \cite{yalniz2019billion}. This model was downloaded from Pytorch hub. For all models, the batch normalization \cite{ioffe2015batch} statistics are kept frozen throughout training and inference. Validation accura...
- We investigate how domain generalization performance is impacted by the choice of iteration $t_0$ when we start model averaging in Eq. \ref{eq_my_sma}. In this section, we simply refer to it as start iteration, which should not be confused with the start of the training process. For experiments, we use the PACS and TerraIncognita datasets. To investigate a wide range of start and end iterations, for all experiments in this section, we train models for $10,000$ iterations.

## wdrdg
- TeX files scanned: `1`
- Approximate TeX word count: `15492`
- Figures: `5`; tables: `4`; algorithms: `1`
- Section sequence: Introduction, Introduction, Preliminaries and Problem Setup, DRO for domain generalization, Wasserstein Distributionally Robust Domain Generalization, Construction of Uncertainty Sets, Balance Robustness and Discriminability, Distributionally Robust Optimization, Adaptive Inference via Optimal Transport, Adaptive Inference by Test-time  Adaptation, Generalization Analysis, Experiments, Datasets, Experimental Configuration, Baseline Methods, Results and Discussion, Ablation Study for the Test-time Adaptation, Analysis of Imbalanced Classes among Source Domains
- Over-explanatory tone hits: {'why ': 2}

Representative opening paragraphs:
- Numerous methods have been developed for learning a generalizable model by exploiting the available data from the source domains, where the shifts across these source domains are implicitly assumed to be representative of the target shift that we will meet at test time. The well-known approaches include learning domain-invariant feature representations through kernel functions \cite{blanchard2011generalizing,muandet2013domain,ghifary2016scatter,blanchard2017domain,grubinger2015domain,li2018domain2,hu2020domain}, or by distribution alignment \cite{zhou2020domain,peng2019moment,motiian2017unified}, or in an adversarial manner \cite{li2018domain...
- Instead, to explicitly model unseen target domain shifts, meta-learning-based domain generalization methods like MLDG \cite{li2018learning} divides the source domains into non-overlapping meta-train and meta-test domains, which fails to hedge against the possible target shift beyond the distribution shifts observed in source domains. Also, these approaches require sufficient source training data to make good meta-optimization within each mini-batch. Possible domain shift could also been modeled by enhancing the diversity of data based on some data augmentations \cite{tobin2017domain}, generating data in an adversarial manner \cite{shankar2018...
- In this work, we propose a domain generalization framework to explicitly model the unknown target domain shift under limited source knowledge, by extrapolating beyond the domain shifts among multiple source domains in a probabilistic setting via distributionally robust optimization (DRO) \cite{bagnell2005robust}. To model the shifts between training and test distributions, DRO usually assumes the testing data is generated by a perturbed distribution of the underlying data distribution, and the perturbation is bounded explicitly by an uncertainty set. It then optimizes the worst-case performance of a model over the uncertainty set to hedge aga...

## fad
- TeX files scanned: `2`
- Approximate TeX word count: `1644`
- Figures: `1`; tables: `0`; algorithms: `0`
- Section sequence: Introduction, Response length, Formatting your Response, Illustrations, graphs, and photographs
- Over-explanatory tone hits: {}

Representative opening paragraphs:
- After receiving paper reviews, authors may optionally submit a rebuttal to address the reviewers' comments, which will be limited to a {\bf one page} PDF file. Please follow the steps and style guidelines outlined below for submitting your author response.
- The author rebuttal is optional and, following similar guidelines to previous CVPR conferences, is meant to provide you with an opportunity to rebut factual errors or to supply additional information requested by the reviewers. It is NOT intended to add new contributions (theorems, algorithms, experiments) that were absent in the original submission and NOT specifically requested by the reviewers. You may optionally add a figure, graph, or proof to your rebuttal to better illustrate your answer to the reviewers' comments.
- Per a passed 2018 PAMI-TC motion, reviewers should refrain from requesting significant additional experiments for the rebuttal or penalize for lack of additional experiments. Authors should refrain from including new experimental results in the rebuttal, especially when not specifically requested to do so by the reviewers. Authors may include figures with illustrations or comparison tables of results reported in the submission/supplemental material or in other papers.

## wilds
- TeX files scanned: `3`
- Approximate TeX word count: `2662`
- Figures: `2`; tables: `0`; algorithms: `0`
- Section sequence: Datasets with distribution shifts that do not cause performance drops, #2, #2, #2
- Over-explanatory tone hits: {}

Representative opening paragraphs:

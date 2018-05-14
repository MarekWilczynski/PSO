function dice_ind = python_RenCystSeg(img_path, params)
%%
PSO_params = struct('AD_N', params(1), ... % 40 % by MW
                    'AD_kappa', params(2), ... % 4.0
                    'AD_lambda', params(3), ... % 0.15
                    'GTstd', params(4), ... % 1.0
                    'cAlpha', params(5), ... % 0.02
                    'cBeta', params(6), ...  % 0.5
                    'dt', params(7), ... % 1.0
                    'mu', params(8), ... % 0.075
                    'Niter', 1,... % def
                    'max_iter', 100,... % def
                    'G_params', struct( ...
                        'G_alpha', params(9), ... % 1.0
                        'G_type', params(10), ... % 0-6 0
                        'G_kernel_dims', ones(1,3) * params(11))); % 2
%%
                
% Pawe³ Badura, Bart³omiej Pyciñski, Wojciech Wiêc³awek 2015
% Algorytm detekcji/segmentacji cyst w nerkach
%   Skrypt g³ówny. Mo¿e byæ wywo³ywany bezpoœrednio lub z zewn¹trz przez funkcjê Fun_RenCystSeg_main z parametrami:
% pathroot - œcie¿ka do katalogu z badaniami pacjenta
% dataData - struktura danych pacjenta (serii) do wczytania. 3 pola: Nr, Yr, Tp
% ARG - struktura z parametrami uruchomienia
% Res - rezultat segmentacji - do przypisania
    
    if ((~exist('WOZI', 'var') || (WOZI ~= 20151125)))
        CZYfunkcja = false;         % UWAGA! Jeœli wywo³anie jest z funkcji zewnêtrznej, to CZYfunkcja z automatu jest równe 1
    end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Inicjalizacja parametrów %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    if (~CZYfunkcja)    
      
        dataData = struct(  'Nr',   104,...
                            'Yr',   12,...
                            'Tp',   'c');
        pathroot = strrep('Obrazy\', '\', filesep);
        CZYfunkcja = false;
    end
    global PAR XYZ
    TIME = [];
    PAR.DISP = struct(  'Profile',          0,...
                        'ImOrig',           0,...
                        'Im',               0,...
                        'LungSeg',          0,...
                        'KidSeg',           0,...
                        'RenCystDet',       0,...
                        'RenCystFineSeg',   0);
    PAR.a = 0.0;
    PAR.ifImWin = 1;                % czy okno intensywnoœci?
        PAR.ImWinRange = [-100, 200];   % granice okna intensywnoœci
    PAR.ifMOrigFeatures = 0;        % czy badamy w³asnoœci maski
    PAR.ifLungSeg = 0;              % czy segmentacja p³uc
        PAR.LungSegMode = 2;        % tryb segmentacji p³uc (z naczyniami/bez naczyñ)
    PAR.ifKidSeg = 1;               % czy segmentacja zal¹¿ków nerek
        PAR.ifKidSegSaveLoad = 2;   % czy zapis/wczytywanie w segmentacji nerek; 0 - normalny tryb; 1 - segmentacja i zapis; 2 - wczytywanie
    PAR.ifKidFeatures = 0;          % czy badamy w³asnoœci nerek
    PAR.ifRenCystDet = 1;           % czy detekcja cyst
        PAR.ifRenCystDetSaveLoad = 0;   % czy zapis/wczytywanie w detekcji cyst; 0 - normalny tryb; 1 - segmentacja i zapis; 2 - wczytywanie
        switch dataData.Tp
            case 'c'
                PAR.RenCystDetThr = [-15, 60];    % progi detekcji cyst
            case 'b'
                PAR.RenCystDetThr = [-15, 55];    % progi detekcji cyst
        end
        PAR.ifRenCystDetSaveTFPN = 0;   % czy zapis obrazków z wynikami detekcji
    PAR.ifRenCystFineSeg = PAR.ifRenCystDet && 1;
        PAR.ifRenCystFineSegSaveTFPN = 0;       
        
    if (PAR.DISP.Profile)   profile on;     end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Aktualizacja œcie¿ki %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    addpath(genpath(cd));
    addpath(genpath(fullfile('..', 'PB_CommonFunctions')));
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Czytanie wolumenu %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    tic;
    ImFileName = strcat('Obrazy\\', img_path);
    MFileName = [ImFileName, '_t.mha'];
    ImFileName = [ImFileName, '.mha'];
    ImInfo = mha_read_header(ImFileName);
    ImOrig = mha_read_volume(ImInfo);
    try
        MInfo = mha_read_header(MFileName);
        MOrig = mha_read_volume(MInfo);
    catch exc
        disp('Nie ma obrysow dla tej serii!!');
        MOrig = zeros(size(ImOrig));
    end
%% Uwaga, wolumen powinien byæ zorientowany tradycyjnie w wymiarach xy, przekroje numerowane od najwy¿szego w wymiarze z
    ImOrig = double(flipdim(permute(ImOrig, [2 1 3]), 3));
    MOrig = logical(flipdim(permute(MOrig, [2 1 3]), 3));
    XYZOrig = ImInfo.PixelDimensions;
    XYZ = XYZOrig;
    TIME.VolRead = toc;
    %disp(['Reading... DONE.   ',num2str(TIME.VolRead),'s']);
    if (PAR.DISP.ImOrig)    
        if (nnz(MOrig)) centrMOrig = Fun_GetCentroid(MOrig);
        else            centrMOrig = size(ImOrig) / 2;
        end
        Fun_DispSlices(ImOrig, MOrig, 22, round(centrMOrig(3)));     
    end
    SUMM.pathFile = img_path;

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Ekstrakcja cech torbieli w masce referencyjnej %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.ifMOrigFeatures)
        tic;
        rpMO = regionprops(MOrig, 'BoundingBox');
        MORenCystNr = numel(rpMO);
        MORC.N = MORenCystNr;
        for rc = 1:MORenCystNr
            MORC.BB(rc, :) = rpMO(rc).BoundingBox;
            bb = ceil(MORC.BB(rc, 1:3));      bb = [bb;   bb + MORC.BB(rc, 4:6) - 1];
            MORC = Fun_GetRenCystFeatures(  ImOrig(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            MOrig(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            MORC,...
                                            rc);
        end
        SUMM.MORC = MORC;
        TIME.MOrigFeatures = toc;
        disp(['Cyst features extraction... DONE.   ',num2str(TIME.MOrigFeatures),'s']);
    end
    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Resampling in X-Y-Z axis
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.a)
        tic;
        DSV = Fun_GetDSV(XYZ, PAR.a);
        Im = Fun_VolResample(Im, DSV);
        M = Fun_VolResample(MOrig, DSV);
        % SeedPoints = Fun_SeedPointsResample(SeedPoints, DSV);
        XYZ = [PAR.a PAR.a PAR.a];
        TIME.Resample = toc;
        %disp(['Resampling... DONE.   ',num2str(TIME.Resample),'s']);
    else
        Im = ImOrig;
        M = MOrig;
    end
    [w,k,g] = size(Im);
    if (nnz(M))     centrM = Fun_GetCentroid(M);
    else            centrM = size(Im) / 2;
    end

    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Inicjalizacja parametrów, ci¹g dalszy %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Elementy strukturalne
    global SE
%     SE.Rmikro_3D = Fun_Strel('ball', 3, 1);
%     SE.Rmin_3D = Fun_Strel('ellipsoid', 3, max(XYZ), XYZ);   % minimalny element strukturalny dwuwymiarowy
    SE.R1_3D = Fun_Strel('ellipsoid', 3, 1, XYZ);
    SE.R2_3D = Fun_Strel('ellipsoid', 3, 2, XYZ);
    SE.R3_3D = Fun_Strel('ellipsoid', 3, 3, XYZ);
    SE.R5_3D = Fun_Strel('ellipsoid', 3, 5, XYZ);
%     SE.R7_3D = Fun_Strel('ellipsoid', 3, 7, XYZ);
%     SE.R8_3D = Fun_Strel('ellipsoid', 3, 8, XYZ);
%     SE.R10_3D = Fun_Strel('ellipsoid', 3, 10, XYZ);
%     SE.R20_3D = Fun_Strel('ellipsoid', 3, 20, XYZ);
%     SE.D1LZ_3D = Fun_Strel('lineins', 3, 1);
    SE.D2LZ_3D = Fun_Strel('lineins', 3, 2);
%     SE.R1_2D = Fun_Strel('disk', 2, Fun_mm2vox(1, XYZ(1)));
    SE.R2_2D = Fun_Strel('disk', 2, Fun_mm2vox(2, XYZ(1)));
%     SE.R3_2D = Fun_Strel('disk', 2, Fun_mm2vox(3, XYZ(1)));
%     SE.R4_2D = Fun_Strel('disk', 2, Fun_mm2vox(4, XYZ(1)));
%     SE.R5_2D = Fun_Strel('disk', 2, Fun_mm2vox(5, XYZ(1)));
%     SE.R10_2D = Fun_Strel('disk', 2, Fun_mm2vox(10, XYZ(1)));


% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %% SeedPoints
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% tic;
% SeedPoints = [];
% % PATHFILEIN
% SeedPoints = Fun_GetSeedPoints(Imwin);
% if (isempty(SeedPoints))
%     msgbox('No seed points! Program terminated.');
%     ImFINAL = [];
%     autotime = 0;
%     SeedPointsFull = [];
%     return;
% end
% SeedPointsFull = SeedPoints;
% tSP = toc;
% disp(['Seed Points... DONE.   ',num2str(tSP),'s']);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Segmentacja p³uc %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.ifLungSeg)
        tic;
        Lungs = Fun_SMP_SegmentacjaPluc(Im, PAR.LungSegMode);
        TIME.LungSeg = toc;
        %disp(['Lungs segmentation... DONE.   ',num2str(TIME.LungSeg),'s']);
        if (PAR.DISP.LungSeg)   Fun_DispSlices(Im, Lungs, 21, 1);   end
    end
    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Okienkowanie intensywnoœci %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.ifImWin)
        tic;
        Im = Fun_ImWindow(Im, PAR.ImWinRange);
        TIME.ImWin = toc;
        %disp(['Image windowing... DONE.   ',num2str(TIME.ImWin),'s']);
    end
    if (PAR.DISP.Im)
        if (PAR.ifMOrigFeatures)        Info = Fun_GetRenCystTextInfo(ImFileName, MORC);
        else                            Info = [];
        end
        Fun_DispSlices(Im, M, 22, round(centrM(3)), Info);
    end
% %     ITIB2016_fig_MissedRenCysts;
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Detekcja nerek (WW) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if (PAR.ifKidSeg)
    tic
    if (PAR.ifKidSegSaveLoad < 2)
%         [KidSmallL, KidBigL, MKidL] = Fun_SMP_SegmentacjaLewejNerkiC(ImOrig, Lungs);
        [KidSmallL, KidBigL, MKidL, KidSmallR, KidBigR, MKidR] = Fun_SMP_SegmentacjaNerekC(ImOrig, Lungs);
        if (PAR.ifKidSegSaveLoad == 1)
            save(fullfile('Res', [SUMM.pathFile, '_KidSeg.mat']),   'KidSmallL', 'KidBigL', 'MKidL',...
                                                                    'KidSmallR', 'KidBigR', 'MKidR');
        end
    else
        load(fullfile('Res', [SUMM.pathFile, '_KidSeg.mat']),   'KidSmallL', 'KidBigL', 'MKidL',...
                                                                'KidSmallR', 'KidBigR', 'MKidR');
    end
    TIME.KidSeg = toc;
    %disp(['Kidneys segmentation... DONE.   ',num2str(TIME.KidSeg),'s']);
    if (PAR.DISP.KidSeg)   Fun_DispSlices(Im, double(KidSmallL|KidSmallR) + 2*double(KidBigL|KidBigR) + 3*double(MKidL|MKidR), 21);   end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Ekstrakcja cech nerek po segmentacji %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.ifKidFeatures)
        tic;
        rpKidSmallL = regionprops(double(KidSmallL), 'BoundingBox');
        KidSmallLNr = numel(rpKidSmallL);
        KSL.N = KidSmallLNr;
        for ks = 1:KidSmallLNr
            KSL.BB(ks, :) = rpKidSmallL(ks).BoundingBox;
            bb = ceil(KSL.BB(ks, 1:3));     bb = [bb;   bb + KSL.BB(ks, 4:6) - 1];
            KSL = Fun_GetRenCystFeatures(   ImOrig(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KidSmallL(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KSL,...
                                            ks);
        end
        SUMM.KSL = KSL;
        rpKidBigL = regionprops(double(KidBigL), 'BoundingBox');
        KidBigLNr = numel(rpKidBigL);
        KBL.N = KidBigLNr;
        for ks = 1:KidBigLNr
            KBL.BB(ks, :) = rpKidBigL(ks).BoundingBox;
            bb = ceil(KBL.BB(ks, 1:3));     bb = [bb;   bb + KBL.BB(ks, 4:6) - 1];
            KBL = Fun_GetRenCystFeatures(   ImOrig(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KidBigL(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KBL,...
                                            ks);
        end
        SUMM.KBL = KBL;

        rpKidSmallR = regionprops(double(KidSmallR), 'BoundingBox');
        KidSmallRNr = numel(rpKidSmallR);
        KSR.N = KidSmallRNr;
        for ks = 1:KidSmallRNr
            KSR.BB(ks, :) = rpKidSmallR(ks).BoundingBox;
            bb = ceil(KSR.BB(ks, 1:3));     bb = [bb;   bb + KSR.BB(ks, 4:6) - 1];
            KSR = Fun_GetRenCystFeatures(   ImOrig(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KidSmallR(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KSR,...
                                            ks);
        end
        SUMM.KSR = KSR;
        rpKidBigR = regionprops(double(KidBigR), 'BoundingBox');
        KidBigRNr = numel(rpKidBigR);
        KBR.N = KidBigRNr;
        for ks = 1:KidBigRNr
            KBR.BB(ks, :) = rpKidBigR(ks).BoundingBox;
            bb = ceil(KBR.BB(ks, 1:3));     bb = [bb;   bb + KBR.BB(ks, 4:6) - 1];
            KBR = Fun_GetRenCystFeatures(   ImOrig(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KidBigR(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                            KBR,...
                                            ks);
        end
        SUMM.KBR = KBR;

        TIME.KidFeatures = toc;
        %disp(['Kidneys features extraction... DONE.   ',num2str(TIME.KidFeatures),'s']);
    end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Detekcja torbieli %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.ifRenCystDet)
        tic;
        if (PAR.ifRenCystDetSaveLoad < 2)
    %         [KidSmallL, KidBigL, MKidL] = Fun_SMP_SegmentacjaLewejNerkiC(ImOrig, Lungs);
            [LRenCyst, rpRenCyst, SUMM] = Fun_RenCystDet(   Im,...
                                                            imdilate(MKidL | MKidR, SE.R5_3D),...
                                                            M,...
                                                            SUMM,...
                                                            dataData);
            if (PAR.ifRenCystDetSaveLoad == 1)
                save(fullfile('Res', [SUMM.pathFile, '_RenCystDet.mat']), 'LRenCyst', 'rpRenCyst', 'SUMM');
            end
        else
            load(fullfile('Res', [SUMM.pathFile, '_RenCystDet.mat']), 'LRenCyst', 'rpRenCyst', 'SUMM');
        end
        TIME.RenCystDet = toc;
        %disp(['Renal cysts detection... DONE.   ',num2str(TIME.RenCystDet),'s']);
%         if (PAR.DISP.RenCystDet)    Fun_DispSlices(Im, RenCyst + 2*M, 21, round(centrM(3)));   end
%         if (PAR.DISP.RenCystDet)    Fun_DispSlices(Im-100*M, bwlabeln(RenCyst), 21, round(centrM(3)));  end
        if (PAR.DISP.RenCystDet)    Fun_DispSlices(Im-100*M, LRenCyst, 21, round(centrM(3)));  end
    end
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Segmentacja torbieli %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if (PAR.ifRenCystFineSeg)
        tic;
        RenCystFine = zeros(size(Im));
        margin = Fun_mm2vox([10 10 10], XYZ);
        Nrc = numel(rpRenCyst);
        for rc = 1:Nrc
            bb = ceil(rpRenCyst(rc).BoundingBox(1:3));  bb = [bb;   bb + rpRenCyst(rc).BoundingBox(4:6) - 1];
            bb = max([1, 1, 1; 1, 1, 1], min([w, k, g; w, k, g], bb + [-margin; margin])); 
            [RCF, SUMM_RCFS(rc)] =  Fun_RenCystFineSeg( Fun_ImCrop(Im, bb(:,[2 1 3])),...
                                    Fun_ImCrop((LRenCyst==rc), bb(:,[2 1 3])),...
                                    Fun_ImCrop(M, bb(:,[2 1 3])), PSO_params);
%             [RCF, SUMM_RCFS(rc)] =  TEST_Fun_RenCystFineSeg( Fun_ImCrop(Im, bb(:,[2 1 3])),...
%                                     Fun_ImCrop((LRenCyst==rc), bb(:,[2 1 3])),...
%                                     Fun_ImCrop(M, bb(:,[2 1 3])));
            if (PAR.ifRenCystFineSegSaveTFPN)
                Fun_SaveImResViawljoin2(Im(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                        0.70 * RCF + 0.30 * M(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
                                        [],...
                                        fullfile('Res', 'FineSeg_TFPN', [[int2str(dataData.Nr), '_', Fun_Nazwa(dataData.Yr, 0, 2), '_', dataData.Tp], '_', Fun_Nazwa(rc, 0, 3), '.png']),...
                                        [1 0 0],...
                                        'sd');
%                 Fun_SaveImResViawljoin2(Im(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3)),...
%                                         0.70 * Fun_Bin2DEdges(RCF) + 0.30 * Fun_Bin2DEdges(M(bb(1,2):bb(2,2), bb(1,1):bb(2,1), bb(1,3):bb(2,3))),...
%                                         [],...
%                                         fullfile('Res', 'FineSeg_TFPN', [[int2str(dataData.Nr), '_', Fun_Nazwa(dataData.Yr, 0, 2), '_', dataData.Tp], '_', Fun_Nazwa(rc, 0, 3), '.png']),...
%                                         [1 0 0],...
%                                         'sd');
            end
            
%             ITIB2016_fig_RenCystFineSeg;
            
            RenCystFine = max(RenCystFine, Fun_ImInsert(zeros(size(RenCystFine)), rc * RCF, bb(:, [2 1 3])));
            if (isfield(SUMM_RCFS(rc), 'TN'))
                SUMM_RCFS(rc).TN = numel(M) - (SUMM_RCFS(rc).TP + SUMM_RCFS(rc).FP + SUMM_RCFS(rc).FN);
            end
        end
        SUMM.RCFS = SUMM_RCFS;
        TIME.RenCystFineSeg = toc;
        %disp(['Renal cysts fine segmentation... DONE.   ',num2str(TIME.RenCystFineSeg),'s']);
    %         if (PAR.DISP.RenCystDet)    Fun_DispSlices(Im, RenCyst + 2*M, 21, round(centrM(3)));   end
        if (PAR.DISP.RenCystFineSeg)    Fun_DispSlices(Im-100*M, bwlabeln(RenCystFine), 21, round(centrM(3)));  end
    end
    
    
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Wstawienie do wolumenu %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    if (PAR.DISP.Profile)   profile viewer;     end
       
    TP = RenCystFine .* MOrig;
    TP = sum(TP(:));
    FP = RenCystFine .* ~MOrig;
    FP = sum(FP(:));
    FN = ~RenCystFine .* MOrig;
    FN = sum(FN(:));
    dice_ind = 2 * TP ./ ( 2 * TP + FP + FN);
    
end
function [Pluca] = Fun_SMP_SegmentacjaPluc(Im, spacing, thr, object_to_remove_size, se1, se2, se3, se4, se5)

	object_to_remove_size = double(object_to_remove_size);

% Pawe� Badura 2013
% Zgrubna segmentacja pluc
% Im - seria CT
% naczynia - czy wersja bez naczy� (1), czy z unaczynieniem (2)?
% thr - opcjonalnie podawany pr�g z zewn�trz. Uwaga, podawany jest bezpo�rednio do u�ycia w progowaniu, ostro�nie z normalizacj�!!
% Pluca - wolumen binarny z maska pluc
% thr - warto��  progu Otsu
% thrHU - warto�� progu Otsu w HU (podejrzane)

    %thrHU = mini + thr * (maksi - mini);        % pr�g Otsu w HU
    Pluca = Im < thr;                           % progowanie
%     Pluca = imopen(Pluca, SE.D2LZ_3D);          % 201512132b: pr�ba pozaklejania dziur w korpusie (raczej nieudana)
    Korpus = ~Pluca;                            % cia�o
%% PONI�SZY FRAGMENT ELIMINUJE OTOCZENIE CIA�A
                                    % czyszczenie brzeg�w na ka�dym przekroju
    Pluca = imclearborder(Pluca);   

    Pluca = imopen(Pluca, se1);            % 20151210: eliminacja refleks�w w mi�sie
    
%% PRZETWARZANIE KORPUSU    
    Korpus = imclose(Korpus, se2);       % 201512132b: pr�ba pozaklejania dziur w korpusie
    Korpus = imclose(Korpus, se3);         % 20151210: eliminacja refleks�w w mi�sie
%     Korpus = imopen(Korpus, SE.R4_2D);          % oderwanie od gantry, aktualnie w�tpliwe
    Korpus = imopen(Korpus, se4);          % oderwanie od gantry
    LKorpus = bwlabeln(Korpus, 8);             % 8 by MW
    
	if(~any(LKorpus))
		Pluca = zeros(size(Pluca));
		return;
	end
    rpKorpus = regionprops(LKorpus, 'Area', 'Centroid', 'BoundingBox');
    [~, maxL] = max([rpKorpus.Area]);
    Korpus = LKorpus == maxL;

%     Korpus = imclose(Korpus, SE.R2_2D);
    Korpus = imdilate(Korpus, se5);

    
    Korpus= imfill(Korpus, 'holes');
    
%     Korpus(:,:,1) = imfill(Korpus(:,:,1), 'holes');
%     Korpus(:,:,end) = imfill(Korpus(:,:,end), 'holes');
%     Korpus = imfill(Korpus, 'holes');
    
    Pluca = Korpus & Pluca;                    % p�uca maskowane korpusem
    
    
% %% PONI�SZY FRAGMENT ELIMINUJE WN�TRZE UK�ADU POKARMOWEGO I INNE  OBIEKTY NIESI�GAJ�CE NAJWY�SZEGO PRZEKROJU
%     L = bwlabeln(Pluca);                        % etykietowanie tego, co zosta�o
% %     L2Bleft = unique(nonzeros(L(:,:,1) .* Pluca(:,:,1)));   % pozostaw tylko te obiekty, kt�re przecinaj� pierwszy przekr�j
%     L2Bleft = unique(nonzeros(L(:,:,1:5) .* Pluca(:,:,1:5)));   % pozostaw tylko te obiekty, kt�re przecinaj� pierwszy przekr�j
%     Pluca = false(w,k,g);
%     for i = 1:numel(L2Bleft)
%         Pluca(L == L2Bleft(i)) = true;
%     end
    
%% PONI�SZY FRAGMENT USUWA MA�E OBIEKTY SPO�R�D POZOSTA�YCH
	object_size = floor(prod(spacing) * object_to_remove_size^2);
    Pluca = bwareaopen(Pluca, object_size);     % usu� b. ma�e (poni�ej 2x2x2cm)
    
    if (nnz(Pluca))
        [L, NL] = bwlabeln(Pluca);                  % etykietowanie tego, co zosta�o
        if (NL > 1)
%% PONI�SZY FRAGMENT WYBIERA 2 NAJWI�KSZE OBIEKTY SPO�R�D POZOSTA�YCH
            RP = regionprops(L, 'Area', 'Centroid', 'BoundingBox');    % cechy obiekt�w
            Areas = [RP.Area];                          % obj�to�ci obiekt�w
            [Areas, Idx] = sort(Areas, 'descend');      % ... posortowane
            %ZcRange = [0.2, 0.8];
            YcRange = [0.2, 0.8];
            %ZcRange = ceil(RP(Idx(1)).BoundingBox(3)) + ZcRange * (RP(Idx(1)).BoundingBox(6) - 1);
            YcRange = ceil(RP(Idx(1)).BoundingBox(2)) + YcRange * (RP(Idx(1)).BoundingBox(4) - 1);
            if     ((RP(Idx(2)).Centroid(2) >= YcRange(1)) && (RP(Idx(2)).Centroid(2) <= YcRange(2)))
					%(RP(Idx(2)).Centroid(3) >= ZcRange(1)) && ...
                    %(RP(Idx(2)).Centroid(3) <= ZcRange(2)) && ...
                    
                Pluca = ((L == Idx(1)) | (L == Idx(2)));    % wybierz najwi�ksze spo�r�d pozosta�ych
            else
                Pluca = (L == Idx(1));                  % wybierz najwi�kszy spo�r�d pozosta�ych
            end
%             Pluca = (L == Idx(1));    % wybierz najwi�kszy spo�r�d pozosta�ych
%         L = bwlabeln(Pluca);                        % etykietowanie tego, co zosta�o
%         RP = regionprops(L, 'Area', 'Centroid');    % cechy obiekt�w
%         Areas = [RP.Area];                          % obj�to�ci obiekt�w
%         [Areas, Idx] = sort(Areas, 'descend');      % ... posortowane
%     %     Pluca = ((L == Idx(1)) | (L == Idx(2)));
%         CentroidsY = [RP(Idx(1:4)).Centroid];       % centroidy pierwszych czterech
%         CentroidsY = CentroidsY(2:3:end);           % ... i ich wsp�rz�dne Y
%         [CentroidsY, Idx2] = sort(CentroidsY, 'descend');       % ... posortowane
%         Pluca = ((L == Idx(Idx2(1))) | (L == Idx(Idx2(2))));    % wybierz zlokalizowane najni�ej
        end
%         if (naczynia == 2)
% %             maxHoleArea = round(2*w);
%             maxHoleArea = round(700 / prod(XYZ(1:2)));             % 20151214 - max dziura w rozmiarach bezwzgl�dnych (ko�o o promieniu ok. 15mm)
%             for i = 1:g
% %                 Pluca(:,:,i) = imclose(Pluca(:,:,i), SE.R2_2D);         % wariant tylko domkni�cia
%                 Pluca(:,:,i) = imclose(Pluca(:,:,i), SE.R4_2D);         % wariant tylko domkni�cia (20151214)
%                 ImF = imfill(Pluca(:,:,i), 'holes');
%                 Pluca(:,:,i) = ImF & ~bwareaopen(~Pluca(:,:,i), maxHoleArea);
%         %         Pluca(:,:,i) = imfill(Pluca(:,:,i), 'holes');           % wariant tylko zalania
%                 Pluca(:,:,i) = imclose(Pluca(:,:,i), SE.R2_2D);         % wariant tylko domkni�cia; do usuni�cia
%             end
%             Pluca = imclose(Pluca, SE.D2LZ_3D);
%         end
    end
end
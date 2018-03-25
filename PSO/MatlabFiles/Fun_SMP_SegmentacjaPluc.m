function [Pluca] = Fun_SMP_SegmentacjaPluc(Im, spacing, thr, object_to_remove_size, se1, se2, se3, se4, se5)

	object_to_remove_size = double(object_to_remove_size);

% Pawe³ Badura 2013
% Zgrubna segmentacja pluc
% Im - seria CT
% naczynia - czy wersja bez naczyñ (1), czy z unaczynieniem (2)?
% thr - opcjonalnie podawany próg z zewn¹trz. Uwaga, podawany jest bezpoœrednio do u¿ycia w progowaniu, ostro¿nie z normalizacj¹!!
% Pluca - wolumen binarny z maska pluc
% thr - wartoœæ  progu Otsu
% thrHU - wartoœæ progu Otsu w HU (podejrzane)

    %thrHU = mini + thr * (maksi - mini);        % próg Otsu w HU
    Pluca = Im < thr;                           % progowanie
%     Pluca = imopen(Pluca, SE.D2LZ_3D);          % 201512132b: próba pozaklejania dziur w korpusie (raczej nieudana)
    Korpus = ~Pluca;                            % cia³o
%% PONI¯SZY FRAGMENT ELIMINUJE OTOCZENIE CIA£A
                                    % czyszczenie brzegów na ka¿dym przekroju
    Pluca = imclearborder(Pluca);   

    Pluca = imopen(Pluca, se1);            % 20151210: eliminacja refleksów w miêsie
    
%% PRZETWARZANIE KORPUSU    
    Korpus = imclose(Korpus, se2);       % 201512132b: próba pozaklejania dziur w korpusie
    Korpus = imclose(Korpus, se3);         % 20151210: eliminacja refleksów w miêsie
%     Korpus = imopen(Korpus, SE.R4_2D);          % oderwanie od gantry, aktualnie w¹tpliwe
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
    
    Pluca = Korpus & Pluca;                    % p³uca maskowane korpusem
    
    
% %% PONI¯SZY FRAGMENT ELIMINUJE WNÊTRZE UK£ADU POKARMOWEGO I INNE  OBIEKTY NIESIÊGAJ¥CE NAJWY¯SZEGO PRZEKROJU
%     L = bwlabeln(Pluca);                        % etykietowanie tego, co zosta³o
% %     L2Bleft = unique(nonzeros(L(:,:,1) .* Pluca(:,:,1)));   % pozostaw tylko te obiekty, które przecinaj¹ pierwszy przekrój
%     L2Bleft = unique(nonzeros(L(:,:,1:5) .* Pluca(:,:,1:5)));   % pozostaw tylko te obiekty, które przecinaj¹ pierwszy przekrój
%     Pluca = false(w,k,g);
%     for i = 1:numel(L2Bleft)
%         Pluca(L == L2Bleft(i)) = true;
%     end
    
%% PONI¯SZY FRAGMENT USUWA MA£E OBIEKTY SPOŒRÓD POZOSTA£YCH
	object_size = floor(prod(spacing) * object_to_remove_size^2);
    Pluca = bwareaopen(Pluca, object_size);     % usuñ b. ma³e (poni¿ej 2x2x2cm)
    
    if (nnz(Pluca))
        [L, NL] = bwlabeln(Pluca);                  % etykietowanie tego, co zosta³o
        if (NL > 1)
%% PONI¯SZY FRAGMENT WYBIERA 2 NAJWIÊKSZE OBIEKTY SPOŒRÓD POZOSTA£YCH
            RP = regionprops(L, 'Area', 'Centroid', 'BoundingBox');    % cechy obiektów
            Areas = [RP.Area];                          % objêtoœci obiektów
            [Areas, Idx] = sort(Areas, 'descend');      % ... posortowane
            %ZcRange = [0.2, 0.8];
            YcRange = [0.2, 0.8];
            %ZcRange = ceil(RP(Idx(1)).BoundingBox(3)) + ZcRange * (RP(Idx(1)).BoundingBox(6) - 1);
            YcRange = ceil(RP(Idx(1)).BoundingBox(2)) + YcRange * (RP(Idx(1)).BoundingBox(4) - 1);
            if     ((RP(Idx(2)).Centroid(2) >= YcRange(1)) && (RP(Idx(2)).Centroid(2) <= YcRange(2)))
					%(RP(Idx(2)).Centroid(3) >= ZcRange(1)) && ...
                    %(RP(Idx(2)).Centroid(3) <= ZcRange(2)) && ...
                    
                Pluca = ((L == Idx(1)) | (L == Idx(2)));    % wybierz najwiêksze spoœród pozosta³ych
            else
                Pluca = (L == Idx(1));                  % wybierz najwiêkszy spoœród pozosta³ych
            end
%             Pluca = (L == Idx(1));    % wybierz najwiêkszy spoœród pozosta³ych
%         L = bwlabeln(Pluca);                        % etykietowanie tego, co zosta³o
%         RP = regionprops(L, 'Area', 'Centroid');    % cechy obiektów
%         Areas = [RP.Area];                          % objêtoœci obiektów
%         [Areas, Idx] = sort(Areas, 'descend');      % ... posortowane
%     %     Pluca = ((L == Idx(1)) | (L == Idx(2)));
%         CentroidsY = [RP(Idx(1:4)).Centroid];       % centroidy pierwszych czterech
%         CentroidsY = CentroidsY(2:3:end);           % ... i ich wspó³rzêdne Y
%         [CentroidsY, Idx2] = sort(CentroidsY, 'descend');       % ... posortowane
%         Pluca = ((L == Idx(Idx2(1))) | (L == Idx(Idx2(2))));    % wybierz zlokalizowane najni¿ej
        end
%         if (naczynia == 2)
% %             maxHoleArea = round(2*w);
%             maxHoleArea = round(700 / prod(XYZ(1:2)));             % 20151214 - max dziura w rozmiarach bezwzglêdnych (ko³o o promieniu ok. 15mm)
%             for i = 1:g
% %                 Pluca(:,:,i) = imclose(Pluca(:,:,i), SE.R2_2D);         % wariant tylko domkniêcia
%                 Pluca(:,:,i) = imclose(Pluca(:,:,i), SE.R4_2D);         % wariant tylko domkniêcia (20151214)
%                 ImF = imfill(Pluca(:,:,i), 'holes');
%                 Pluca(:,:,i) = ImF & ~bwareaopen(~Pluca(:,:,i), maxHoleArea);
%         %         Pluca(:,:,i) = imfill(Pluca(:,:,i), 'holes');           % wariant tylko zalania
%                 Pluca(:,:,i) = imclose(Pluca(:,:,i), SE.R2_2D);         % wariant tylko domkniêcia; do usuniêcia
%             end
%             Pluca = imclose(Pluca, SE.D2LZ_3D);
%         end
    end
end
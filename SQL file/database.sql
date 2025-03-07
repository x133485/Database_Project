PGDMP                      }            database_Project    16.6    16.6 .    .           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            /           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            0           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            1           1262    16781    database_Project    DATABASE     �   CREATE DATABASE "database_Project" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Chinese (Simplified)_China.936';
 "   DROP DATABASE "database_Project";
                postgres    false            �            1259    16899    coaching    TABLE     �   CREATE TABLE public.coaching (
    coach_id integer NOT NULL,
    name character varying(100),
    expertise character varying(100)
);
    DROP TABLE public.coaching;
       public         heap    postgres    false            �            1259    16944    coaching_event    TABLE     g   CREATE TABLE public.coaching_event (
    coach_id integer NOT NULL,
    event_code integer NOT NULL
);
 "   DROP TABLE public.coaching_event;
       public         heap    postgres    false            �            1259    16904 	   equipment    TABLE     �   CREATE TABLE public.equipment (
    equipment_id integer NOT NULL,
    description character varying(255),
    value numeric(10,2),
    quantity integer,
    event_code integer
);
    DROP TABLE public.equipment;
       public         heap    postgres    false            �            1259    16889    events    TABLE     �   CREATE TABLE public.events (
    event_code integer NOT NULL,
    event_description character varying(255),
    event_type character varying(100),
    event_status character varying(50)
);
    DROP TABLE public.events;
       public         heap    postgres    false            �            1259    17005    event_equipment_summary    VIEW     |  CREATE VIEW public.event_equipment_summary AS
 SELECT e.event_code,
    e.event_description,
    COALESCE(sum(eq.value), (0)::numeric) AS total_value,
    COALESCE(sum(eq.quantity), (0)::bigint) AS total_quantity
   FROM (public.events e
     LEFT JOIN public.equipment eq ON ((e.event_code = eq.event_code)))
  GROUP BY e.event_code, e.event_description
  ORDER BY e.event_code;
 *   DROP VIEW public.event_equipment_summary;
       public          postgres    false    216    216    219    219    219            �            1259    16929    event_participant    TABLE     p   CREATE TABLE public.event_participant (
    participant_id integer NOT NULL,
    event_code integer NOT NULL
);
 %   DROP TABLE public.event_participant;
       public         heap    postgres    false            �            1259    16894    participant    TABLE     �   CREATE TABLE public.participant (
    participant_id integer NOT NULL,
    name character varying(100),
    contact_information character varying(255)
);
    DROP TABLE public.participant;
       public         heap    postgres    false            �            1259    17011    users    TABLE     �   CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    17010    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    225            2           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    224            �            1259    16914    volunteer_event    TABLE     �   CREATE TABLE public.volunteer_event (
    volun_id integer NOT NULL,
    event_code integer NOT NULL,
    start_time timestamp without time zone,
    end_time timestamp without time zone
);
 #   DROP TABLE public.volunteer_event;
       public         heap    postgres    false            �            1259    16884 
   volunteers    TABLE     �   CREATE TABLE public.volunteers (
    volun_id integer NOT NULL,
    name character varying(100),
    address character varying(255),
    telephonenumber character varying(50)
);
    DROP TABLE public.volunteers;
       public         heap    postgres    false            t           2604    17014    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    224    225    225            %          0    16899    coaching 
   TABLE DATA           =   COPY public.coaching (coach_id, name, expertise) FROM stdin;
    public          postgres    false    218   �8       )          0    16944    coaching_event 
   TABLE DATA           >   COPY public.coaching_event (coach_id, event_code) FROM stdin;
    public          postgres    false    222   �9       &          0    16904 	   equipment 
   TABLE DATA           [   COPY public.equipment (equipment_id, description, value, quantity, event_code) FROM stdin;
    public          postgres    false    219   �9       (          0    16929    event_participant 
   TABLE DATA           G   COPY public.event_participant (participant_id, event_code) FROM stdin;
    public          postgres    false    221   �:       #          0    16889    events 
   TABLE DATA           Y   COPY public.events (event_code, event_description, event_type, event_status) FROM stdin;
    public          postgres    false    216   �:       $          0    16894    participant 
   TABLE DATA           P   COPY public.participant (participant_id, name, contact_information) FROM stdin;
    public          postgres    false    217   ~;       +          0    17011    users 
   TABLE DATA           A   COPY public.users (user_id, username, password_hash) FROM stdin;
    public          postgres    false    225   �<       '          0    16914    volunteer_event 
   TABLE DATA           U   COPY public.volunteer_event (volun_id, event_code, start_time, end_time) FROM stdin;
    public          postgres    false    220   �<       "          0    16884 
   volunteers 
   TABLE DATA           N   COPY public.volunteers (volun_id, name, address, telephonenumber) FROM stdin;
    public          postgres    false    215   ;=       3           0    0    users_user_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);
          public          postgres    false    224            �           2606    16948 "   coaching_event coaching_event_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.coaching_event
    ADD CONSTRAINT coaching_event_pkey PRIMARY KEY (coach_id, event_code);
 L   ALTER TABLE ONLY public.coaching_event DROP CONSTRAINT coaching_event_pkey;
       public            postgres    false    222    222            |           2606    16903    coaching coaching_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.coaching
    ADD CONSTRAINT coaching_pkey PRIMARY KEY (coach_id);
 @   ALTER TABLE ONLY public.coaching DROP CONSTRAINT coaching_pkey;
       public            postgres    false    218            ~           2606    16908    equipment equipment_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (equipment_id);
 B   ALTER TABLE ONLY public.equipment DROP CONSTRAINT equipment_pkey;
       public            postgres    false    219            �           2606    16933 (   event_participant event_participant_pkey 
   CONSTRAINT     ~   ALTER TABLE ONLY public.event_participant
    ADD CONSTRAINT event_participant_pkey PRIMARY KEY (participant_id, event_code);
 R   ALTER TABLE ONLY public.event_participant DROP CONSTRAINT event_participant_pkey;
       public            postgres    false    221    221            x           2606    16893    events events_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (event_code);
 <   ALTER TABLE ONLY public.events DROP CONSTRAINT events_pkey;
       public            postgres    false    216            z           2606    16898    participant participant_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pkey PRIMARY KEY (participant_id);
 F   ALTER TABLE ONLY public.participant DROP CONSTRAINT participant_pkey;
       public            postgres    false    217            �           2606    17016    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    225            �           2606    17018    users users_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
       public            postgres    false    225            �           2606    16918 $   volunteer_event volunteer_event_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.volunteer_event
    ADD CONSTRAINT volunteer_event_pkey PRIMARY KEY (volun_id, event_code);
 N   ALTER TABLE ONLY public.volunteer_event DROP CONSTRAINT volunteer_event_pkey;
       public            postgres    false    220    220            v           2606    16888    volunteers volunteers_pkey 
   CONSTRAINT     ^   ALTER TABLE ONLY public.volunteers
    ADD CONSTRAINT volunteers_pkey PRIMARY KEY (volun_id);
 D   ALTER TABLE ONLY public.volunteers DROP CONSTRAINT volunteers_pkey;
       public            postgres    false    215            �           1259    16960     idx_event_participant_event_code    INDEX     d   CREATE INDEX idx_event_participant_event_code ON public.event_participant USING btree (event_code);
 4   DROP INDEX public.idx_event_participant_event_code;
       public            postgres    false    221                       1259    16961    idx_volunteer_event_event_code    INDEX     `   CREATE INDEX idx_volunteer_event_event_code ON public.volunteer_event USING btree (event_code);
 2   DROP INDEX public.idx_volunteer_event_event_code;
       public            postgres    false    220            �           2606    16949 +   coaching_event coaching_event_coach_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.coaching_event
    ADD CONSTRAINT coaching_event_coach_id_fkey FOREIGN KEY (coach_id) REFERENCES public.coaching(coach_id);
 U   ALTER TABLE ONLY public.coaching_event DROP CONSTRAINT coaching_event_coach_id_fkey;
       public          postgres    false    222    218    4732            �           2606    16954 -   coaching_event coaching_event_event_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.coaching_event
    ADD CONSTRAINT coaching_event_event_code_fkey FOREIGN KEY (event_code) REFERENCES public.events(event_code);
 W   ALTER TABLE ONLY public.coaching_event DROP CONSTRAINT coaching_event_event_code_fkey;
       public          postgres    false    222    216    4728            �           2606    16909 #   equipment equipment_event_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_event_code_fkey FOREIGN KEY (event_code) REFERENCES public.events(event_code);
 M   ALTER TABLE ONLY public.equipment DROP CONSTRAINT equipment_event_code_fkey;
       public          postgres    false    219    4728    216            �           2606    16939 3   event_participant event_participant_event_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_participant
    ADD CONSTRAINT event_participant_event_code_fkey FOREIGN KEY (event_code) REFERENCES public.events(event_code);
 ]   ALTER TABLE ONLY public.event_participant DROP CONSTRAINT event_participant_event_code_fkey;
       public          postgres    false    221    216    4728            �           2606    16934 7   event_participant event_participant_participant_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.event_participant
    ADD CONSTRAINT event_participant_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(participant_id);
 a   ALTER TABLE ONLY public.event_participant DROP CONSTRAINT event_participant_participant_id_fkey;
       public          postgres    false    217    221    4730            �           2606    16924 /   volunteer_event volunteer_event_event_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.volunteer_event
    ADD CONSTRAINT volunteer_event_event_code_fkey FOREIGN KEY (event_code) REFERENCES public.events(event_code);
 Y   ALTER TABLE ONLY public.volunteer_event DROP CONSTRAINT volunteer_event_event_code_fkey;
       public          postgres    false    220    4728    216            �           2606    16919 -   volunteer_event volunteer_event_volun_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.volunteer_event
    ADD CONSTRAINT volunteer_event_volun_id_fkey FOREIGN KEY (volun_id) REFERENCES public.volunteers(volun_id);
 W   ALTER TABLE ONLY public.volunteer_event DROP CONSTRAINT volunteer_event_volun_id_fkey;
       public          postgres    false    215    220    4726            %   �   x�5��N�0F���� �?���6���N�4qcZ�zd��&���dE�Z��9Ԭ���cq�
J��j ��4��=E��A�5<�/��P��S��nYΏ7P����P�QI\l�_�ϣ[xƉ{�����n>����˄��`#���m�&��}���cw	��G�Z
�y��<�J1����m��H�[\�f��*�iM=w,daM�M9)d{���=.ڢ�ჺ0Q��'�=��|^c~�ks      )      x�3�4����� y"      &   �   x�E���0D�ӯ�Hy����Rc��	��7�X
��|��=���	q^��%���,"�}�p4W��>�һH��p�)JZ�b���;I�X\l�b��͝Z�T/BvT����g��Ai�@B g1
��dU'�W�R���A��	��[�ލ��"?\�\��j6ڻ5=~�)�QY�&ו�5>c��K=�      (      x�3�4����� ]      #   �   x�UPˎ�0<;_�/@�K��b9!$������h�jS����8x4�X3#�?��jr�곩\j��Hب|������9���ޖ��.w����`�@�B|G��
v��j֧�5\��g�C�d��c[M�Gzj��Y����T��Df7���u��)���i�`#u����d�y�<�����=������L)��or�      $   
  x�]��N�0�ϓ���H�� �R�IM��(�iӧ�+N�i�Ռ4��⦭K�VF[� ������6,�Kf�u��k�����9V����j˶B���!,�o�;��0b�	��L]K��<��!�G�9z���z|	�!�/��9ܒyɨ���i�%2m�Q�8A)�"��Q��C=�T�XMS<s��z���}��t�\;�&EZ��w�"�c�+�*�����Ixa[����
�qb8����0�ä�cy��-N�V{��_G�'%I���;      +   R   x�3�LL����T1JT10U�(�3�Is/t*6v��6���M5�,�5�tqO�L�v		Ls�p��)�)������� -�h      '   1   x�3�4��".CN#(˄Ә����T��H��\���
���q��qqq ��.      "   -  x����n�0D�����ر��P+�r@�zq�U,BB�$U���ĵ{\���E�ˣk��_�op�=`����*ӹI��Y���h���|�f��\gJ���J�]��ým��ĸ�',7�%p΅)�0�����ar��(}�&xRJ�TF�2Xۜp�]��U6�n���$���z�o!Ww��Ǥ>L�:~A,y+���É�Q<����D_��{B��|����U[��O�V�2I�a�RR��J����;�߮� �scLB�,K��@���K��.@k}������#c�V_z�     
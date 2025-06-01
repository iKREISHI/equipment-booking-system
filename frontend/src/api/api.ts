/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

/**
 * * `M` - Мужской
 * * `F` - Женский
 * * `U` - Не указан
 */
export enum GenderEnum {
  M = "M",
  F = "F",
  U = "U",
}

/**
 * Сериализатор инвентарного оборудования.
 *
 * * На запись принимает **id** связанных объектов (`owner`, `status`, `location`).
 * * На чтение дополнительно отдаёт их «читаемые» имена.
 */
export interface InventoryEquipment {
  id: number;
  /** ID пользователя-владельца */
  owner: number;
  /** ID статуса оборудования */
  status?: number | null;
  /** ID местоположения оборудования */
  location: number;
  owner_username: string;
  status_name: string;
  location_name: string;
  /**
   * Название инвентарного оборудования
   * @maxLength 100
   */
  name: string;
  /**
   * Штрихкод оборудования
   * @maxLength 32
   */
  inventory_number: string;
  /**
   * Фото оборудования
   * @format uri
   */
  photo?: string | null;
  /** Описание оборудования */
  description?: string | null;
  /**
   * Дата создания
   * @format date
   */
  registration_date: string;
  /**
   * Дата создания
   * @format date
   */
  created_at: string | null;
  /**
   * Дата обновления
   * @format date
   */
  updated_at: string | null;
}

/**
 * Сериализатор статуса инвентарного оборудования.
 * Передаёт / принимает только поле ``name`` (и ``id`` как read-only).
 */
export interface InventoryEquipmentStatus {
  id: number;
  /**
   * Название статуса оборудования
   * @maxLength 64
   */
  name: string;
}

/**
 * Сериализатор местоположения инвентарного оборудования.
 * Отдаёт / принимает поля: id, name, description.
 */
export interface Location {
  id: number;
  /**
   * Название местоположения
   * @maxLength 255
   */
  name: string;
  /** Описание местоположения */
  description: string;
}

export interface Login {
  username: string;
  password: string;
}

/**
 * Сериализатор для модели Maintenance — обслуживания/проверки оборудования.
 * Поля:
 *   - equipment: ссылка на InventoryEquipment (PrimaryKey)
 *   - reporter_by: ссылка на User, кто сообщил о проверке
 *   - assigned_by: ссылка на User, кто выполнял проверку
 *   - description: описание самой проверки (может быть пустым)
 *   - status: ссылка на MaintenanceStatus
 *   - created_at: автоматически ставится при создании (только для чтения)
 *   - updated_at: автоматически обновляется при изменении (только для чтения)
 *   - description_updated: описание изменений (может быть пустым)
 *   - start_time: дата и время начала обслуживания
 *   - end_time: дата и время конца обслуживания
 */
export interface Maintenance {
  id: number;
  /** Инвентарное оборудование */
  equipment: number;
  /** Оборудование (строка) */
  equipment_display: string;
  /** Кто сообщил о проверке оборудования */
  reporter_by: number;
  /** Reporter (строка) */
  reporter_display: string;
  /** Кто проверил исправность оборудования */
  assigned_by: number;
  /** Assigned (строка) */
  assigned_display: string;
  /** Описание проверки оборудования */
  description?: string | null;
  /** Статус обслуживания */
  status: number;
  /** Статус (строка) */
  status_display: string;
  /**
   * Дата и время создания <UNK> <UNK>
   * @format date-time
   */
  created_at: string;
  /**
   * Дата и время обновления
   * @format date-time
   */
  updated_at: string;
  /** Описание обновления */
  description_updated?: string | null;
  /**
   * Дата и время начала обслуживания
   * @format date-time
   */
  start_time: string;
  /**
   * Дата и время конца обслуживания
   * @format date-time
   */
  end_time: string;
}

/**
 * Сериализатор для модели MaintenanceStatus.
 * Позволяет получать и обновлять поля name и description.
 */
export interface MaintenanceStatus {
  id: number;
  /**
   * Название статуса
   * @maxLength 255
   */
  name: string;
  /** Описание */
  description?: string | null;
}

export interface PaginatedInventoryEquipmentList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: InventoryEquipment[];
}

export interface PaginatedInventoryEquipmentStatusList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: InventoryEquipmentStatus[];
}

export interface PaginatedLocationList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: Location[];
}

export interface PaginatedMaintenanceList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: Maintenance[];
}

export interface PaginatedMaintenanceStatusList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: MaintenanceStatus[];
}

export interface PaginatedReservationList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: Reservation[];
}

export interface PaginatedUserList {
  /** @example 123 */
  count: number;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=4"
   */
  next?: string | null;
  /**
   * @format uri
   * @example "http://api.example.org/accounts/?page=2"
   */
  previous?: string | null;
  results: User[];
}

/**
 * Сериализатор инвентарного оборудования.
 *
 * * На запись принимает **id** связанных объектов (`owner`, `status`, `location`).
 * * На чтение дополнительно отдаёт их «читаемые» имена.
 */
export interface PatchedInventoryEquipment {
  id?: number;
  /** ID пользователя-владельца */
  owner?: number;
  /** ID статуса оборудования */
  status?: number | null;
  /** ID местоположения оборудования */
  location?: number;
  owner_username?: string;
  status_name?: string;
  location_name?: string;
  /**
   * Название инвентарного оборудования
   * @maxLength 100
   */
  name?: string;
  /**
   * Штрихкод оборудования
   * @maxLength 32
   */
  inventory_number?: string;
  /**
   * Фото оборудования
   * @format uri
   */
  photo?: string | null;
  /** Описание оборудования */
  description?: string | null;
  /**
   * Дата создания
   * @format date
   */
  registration_date?: string;
  /**
   * Дата создания
   * @format date
   */
  created_at?: string | null;
  /**
   * Дата обновления
   * @format date
   */
  updated_at?: string | null;
}

/**
 * Сериализатор статуса инвентарного оборудования.
 * Передаёт / принимает только поле ``name`` (и ``id`` как read-only).
 */
export interface PatchedInventoryEquipmentStatus {
  id?: number;
  /**
   * Название статуса оборудования
   * @maxLength 64
   */
  name?: string;
}

/**
 * Сериализатор местоположения инвентарного оборудования.
 * Отдаёт / принимает поля: id, name, description.
 */
export interface PatchedLocation {
  id?: number;
  /**
   * Название местоположения
   * @maxLength 255
   */
  name?: string;
  /** Описание местоположения */
  description?: string;
}

/**
 * Сериализатор для модели Maintenance — обслуживания/проверки оборудования.
 * Поля:
 *   - equipment: ссылка на InventoryEquipment (PrimaryKey)
 *   - reporter_by: ссылка на User, кто сообщил о проверке
 *   - assigned_by: ссылка на User, кто выполнял проверку
 *   - description: описание самой проверки (может быть пустым)
 *   - status: ссылка на MaintenanceStatus
 *   - created_at: автоматически ставится при создании (только для чтения)
 *   - updated_at: автоматически обновляется при изменении (только для чтения)
 *   - description_updated: описание изменений (может быть пустым)
 *   - start_time: дата и время начала обслуживания
 *   - end_time: дата и время конца обслуживания
 */
export interface PatchedMaintenance {
  id?: number;
  /** Инвентарное оборудование */
  equipment?: number;
  /** Оборудование (строка) */
  equipment_display?: string;
  /** Кто сообщил о проверке оборудования */
  reporter_by?: number;
  /** Reporter (строка) */
  reporter_display?: string;
  /** Кто проверил исправность оборудования */
  assigned_by?: number;
  /** Assigned (строка) */
  assigned_display?: string;
  /** Описание проверки оборудования */
  description?: string | null;
  /** Статус обслуживания */
  status?: number;
  /** Статус (строка) */
  status_display?: string;
  /**
   * Дата и время создания <UNK> <UNK>
   * @format date-time
   */
  created_at?: string;
  /**
   * Дата и время обновления
   * @format date-time
   */
  updated_at?: string;
  /** Описание обновления */
  description_updated?: string | null;
  /**
   * Дата и время начала обслуживания
   * @format date-time
   */
  start_time?: string;
  /**
   * Дата и время конца обслуживания
   * @format date-time
   */
  end_time?: string;
}

/**
 * Сериализатор для модели MaintenanceStatus.
 * Позволяет получать и обновлять поля name и description.
 */
export interface PatchedMaintenanceStatus {
  id?: number;
  /**
   * Название статуса
   * @maxLength 255
   */
  name?: string;
  /** Описание */
  description?: string | null;
}

/**
 * Сериализатор аренды инвентарного оборудования.
 *
 * • На запись принимает `equipment`, `renter`, `assigned_by`, `location`
 *   как **ID** связанных объектов.
 * • Отдаёт читаемые поля: имя оборудования, пользователи, локация.
 * • Валидирует даты и проверяет перекрытия для одного и того же оборудования.
 */
export interface PatchedReservation {
  id?: number;
  /** ID оборудования */
  equipment?: number;
  /** ID арендатора */
  renter?: number;
  /** ID пользователя, оформившего аренду */
  assigned_by?: number;
  /** ID местоположения оборудования */
  location?: number;
  equipment_name?: string;
  renter_username?: string;
  assigned_by_username?: string;
  location_name?: string;
  /**
   * Время начала
   * @format date-time
   */
  start_time?: string;
  /**
   * Время окончания
   * @format date-time
   */
  end_time?: string;
  /**
   * Фактическое время возврата
   * @format date-time
   */
  actual_return_time?: string | null;
  /** Описание аренды */
  description?: string | null;
}

export interface PatchedSetActive {
  is_active?: boolean;
}

export interface PatchedUser {
  id?: number;
  /**
   * Имя пользователя
   * @maxLength 128
   */
  username?: string;
  /**
   * Почта
   * @format email
   * @maxLength 254
   */
  email?: string | null;
  /**
   * Фамилия
   * @maxLength 150
   */
  last_name?: string;
  /**
   * Имя
   * @maxLength 150
   */
  first_name?: string;
  /**
   * Отчество
   * @maxLength 150
   */
  patronymic?: string | null;
  /** Пол */
  gender?: GenderEnum;
  /**
   * Номер телефона
   * @maxLength 20
   */
  phone?: string | null;
  /**
   * Чат ID телеграмма для отправки уведомлений
   * @maxLength 255
   */
  telegram_chat_id?: string | null;
  /**
   * Аватар
   * @format uri
   */
  avatar?: string | null;
}

/**
 * Сериализатор аренды инвентарного оборудования.
 *
 * • На запись принимает `equipment`, `renter`, `assigned_by`, `location`
 *   как **ID** связанных объектов.
 * • Отдаёт читаемые поля: имя оборудования, пользователи, локация.
 * • Валидирует даты и проверяет перекрытия для одного и того же оборудования.
 */
export interface Reservation {
  id: number;
  /** ID оборудования */
  equipment: number;
  /** ID арендатора */
  renter: number;
  /** ID пользователя, оформившего аренду */
  assigned_by: number;
  /** ID местоположения оборудования */
  location: number;
  equipment_name: string;
  renter_username: string;
  assigned_by_username: string;
  location_name: string;
  /**
   * Время начала
   * @format date-time
   */
  start_time: string;
  /**
   * Время окончания
   * @format date-time
   */
  end_time: string;
  /**
   * Фактическое время возврата
   * @format date-time
   */
  actual_return_time?: string | null;
  /** Описание аренды */
  description?: string | null;
}

export interface User {
  id: number;
  /**
   * Имя пользователя
   * @maxLength 128
   */
  username: string;
  /**
   * Почта
   * @format email
   * @maxLength 254
   */
  email?: string | null;
  /**
   * Фамилия
   * @maxLength 150
   */
  last_name: string;
  /**
   * Имя
   * @maxLength 150
   */
  first_name: string;
  /**
   * Отчество
   * @maxLength 150
   */
  patronymic?: string | null;
  /** Пол */
  gender?: GenderEnum;
  /**
   * Номер телефона
   * @maxLength 20
   */
  phone?: string | null;
  /**
   * Чат ID телеграмма для отправки уведомлений
   * @maxLength 255
   */
  telegram_chat_id?: string | null;
  /**
   * Аватар
   * @format uri
   */
  avatar?: string | null;
}

export interface UserRegistration {
  /**
   * Имя пользователя
   * @maxLength 128
   */
  username: string;
  password: string;
  /** Подтверждение пароля */
  password2: string;
  /**
   * Фамилия
   * @maxLength 150
   */
  last_name: string;
  /**
   * Имя
   * @maxLength 150
   */
  first_name: string;
  /**
   * Отчество
   * @maxLength 150
   */
  patronymic?: string | null;
  /** Пол */
  gender?: GenderEnum;
  /**
   * Почта
   * @format email
   * @maxLength 254
   */
  email?: string | null;
  /**
   * Номер телефона
   * @maxLength 20
   */
  phone?: string | null;
  /**
   * Аватар
   * @format uri
   */
  avatar?: string | null;
}

export type QueryParamsType = Record<string | number, any>;
export type ResponseFormat = keyof Omit<Body, "body" | "bodyUsed">;

export interface FullRequestParams extends Omit<RequestInit, "body"> {
  /** set parameter to `true` for call `securityWorker` for this request */
  secure?: boolean;
  /** request path */
  path: string;
  /** content type of request body */
  type?: ContentType;
  /** query params */
  query?: QueryParamsType;
  /** format of response (i.e. response.json() -> format: "json") */
  format?: ResponseFormat;
  /** request body */
  body?: unknown;
  /** base url */
  baseUrl?: string;
  /** request cancellation token */
  cancelToken?: CancelToken;
}

export type RequestParams = Omit<
  FullRequestParams,
  "body" | "method" | "query" | "path"
>;

export interface ApiConfig<SecurityDataType = unknown> {
  baseUrl?: string;
  baseApiParams?: Omit<RequestParams, "baseUrl" | "cancelToken" | "signal">;
  securityWorker?: (
    securityData: SecurityDataType | null,
  ) => Promise<RequestParams | void> | RequestParams | void;
  customFetch?: typeof fetch;
}

export interface HttpResponse<D extends unknown, E extends unknown = unknown>
  extends Response {
  data: D;
  error: E;
}

type CancelToken = Symbol | string | number;

export enum ContentType {
  Json = "application/json",
  FormData = "multipart/form-data",
  UrlEncoded = "application/x-www-form-urlencoded",
  Text = "text/plain",
}

export class HttpClient<SecurityDataType = unknown> {
  public baseUrl: string = "";
  private securityData: SecurityDataType | null = null;
  private securityWorker?: ApiConfig<SecurityDataType>["securityWorker"];
  private abortControllers = new Map<CancelToken, AbortController>();
  private customFetch = (...fetchParams: Parameters<typeof fetch>) =>
    fetch(...fetchParams);

  private baseApiParams: RequestParams = {
    credentials: "same-origin",
    headers: {},
    redirect: "follow",
    referrerPolicy: "no-referrer",
  };

  constructor(apiConfig: ApiConfig<SecurityDataType> = {}) {
    Object.assign(this, apiConfig);
  }

  public setSecurityData = (data: SecurityDataType | null) => {
    this.securityData = data;
  };

  protected encodeQueryParam(key: string, value: any) {
    const encodedKey = encodeURIComponent(key);
    return `${encodedKey}=${encodeURIComponent(typeof value === "number" ? value : `${value}`)}`;
  }

  protected addQueryParam(query: QueryParamsType, key: string) {
    return this.encodeQueryParam(key, query[key]);
  }

  protected addArrayQueryParam(query: QueryParamsType, key: string) {
    const value = query[key];
    return value.map((v: any) => this.encodeQueryParam(key, v)).join("&");
  }

  protected toQueryString(rawQuery?: QueryParamsType): string {
    const query = rawQuery || {};
    const keys = Object.keys(query).filter(
      (key) => "undefined" !== typeof query[key],
    );
    return keys
      .map((key) =>
        Array.isArray(query[key])
          ? this.addArrayQueryParam(query, key)
          : this.addQueryParam(query, key),
      )
      .join("&");
  }

  protected addQueryParams(rawQuery?: QueryParamsType): string {
    const queryString = this.toQueryString(rawQuery);
    return queryString ? `?${queryString}` : "";
  }

  private contentFormatters: Record<ContentType, (input: any) => any> = {
    [ContentType.Json]: (input: any) =>
      input !== null && (typeof input === "object" || typeof input === "string")
        ? JSON.stringify(input)
        : input,
    [ContentType.Text]: (input: any) =>
      input !== null && typeof input !== "string"
        ? JSON.stringify(input)
        : input,
    [ContentType.FormData]: (input: any) =>
      Object.keys(input || {}).reduce((formData, key) => {
        const property = input[key];
        formData.append(
          key,
          property instanceof Blob
            ? property
            : typeof property === "object" && property !== null
              ? JSON.stringify(property)
              : `${property}`,
        );
        return formData;
      }, new FormData()),
    [ContentType.UrlEncoded]: (input: any) => this.toQueryString(input),
  };

  protected mergeRequestParams(
    params1: RequestParams,
    params2?: RequestParams,
  ): RequestParams {
    return {
      ...this.baseApiParams,
      ...params1,
      ...(params2 || {}),
      headers: {
        ...(this.baseApiParams.headers || {}),
        ...(params1.headers || {}),
        ...((params2 && params2.headers) || {}),
      },
    };
  }

  protected createAbortSignal = (
    cancelToken: CancelToken,
  ): AbortSignal | undefined => {
    if (this.abortControllers.has(cancelToken)) {
      const abortController = this.abortControllers.get(cancelToken);
      if (abortController) {
        return abortController.signal;
      }
      return void 0;
    }

    const abortController = new AbortController();
    this.abortControllers.set(cancelToken, abortController);
    return abortController.signal;
  };

  public abortRequest = (cancelToken: CancelToken) => {
    const abortController = this.abortControllers.get(cancelToken);

    if (abortController) {
      abortController.abort();
      this.abortControllers.delete(cancelToken);
    }
  };

  public request = async <T = any, E = any>({
    body,
    secure,
    path,
    type,
    query,
    format,
    baseUrl,
    cancelToken,
    ...params
  }: FullRequestParams): Promise<HttpResponse<T, E>> => {
    const secureParams =
      ((typeof secure === "boolean" ? secure : this.baseApiParams.secure) &&
        this.securityWorker &&
        (await this.securityWorker(this.securityData))) ||
      {};
    const requestParams = this.mergeRequestParams(params, secureParams);
    const queryString = query && this.toQueryString(query);
    const payloadFormatter = this.contentFormatters[type || ContentType.Json];
    const responseFormat = format || requestParams.format;

    return this.customFetch(
      `${baseUrl || this.baseUrl || ""}${path}${queryString ? `?${queryString}` : ""}`,
      {
        ...requestParams,
        headers: {
          ...(requestParams.headers || {}),
          ...(type && type !== ContentType.FormData
            ? { "Content-Type": type }
            : {}),
        },
        signal:
          (cancelToken
            ? this.createAbortSignal(cancelToken)
            : requestParams.signal) || null,
        body:
          typeof body === "undefined" || body === null
            ? null
            : payloadFormatter(body),
      },
    ).then(async (response) => {
      const r = response.clone() as HttpResponse<T, E>;
      r.data = null as unknown as T;
      r.error = null as unknown as E;

      const data = !responseFormat
        ? r
        : await response[responseFormat]()
            .then((data) => {
              if (r.ok) {
                r.data = data;
              } else {
                r.error = data;
              }
              return r;
            })
            .catch((e) => {
              r.error = e;
              return r;
            });

      if (cancelToken) {
        this.abortControllers.delete(cancelToken);
      }

      if (!response.ok) throw data;
      return data;
    });
  };
}

/**
 * @title Equipment booking system API
 * @version 1.0.0
 *
 * Equipment booking system for Technopark SHSPU
 */
export class Api<
  SecurityDataType extends unknown,
> extends HttpClient<SecurityDataType> {
  api = {
    /**
     * @description Поддерживает фильтры: - `owner` — ID владельца - `status` — ID статуса - `location` — ID местоположения И поиск по `name` или `inventory_number` через `?search=`.
     *
     * @tags v0
     * @name V0InventoryEquipmentList
     * @summary Список инвентарного оборудования
     * @request GET:/api/v0/inventory-equipment/
     * @secure
     */
    v0InventoryEquipmentList: (
      query?: {
        location?: number;
        owner?: number;
        page?: number;
        page_size?: number;
        search?: string;
        status?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedInventoryEquipmentList, any>({
        path: `/api/v0/inventory-equipment/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для **InventoryEquipment**. | Операция               | Model-permission | |------------------------|------------------| | list / retrieve        | `view_inventoryequipment` | | create                 | `add_inventoryequipment` | | update / partial_update| `change_inventoryequipment` | | destroy                | `delete_inventoryequipment` |
     *
     * @tags v0
     * @name V0InventoryEquipmentCreate
     * @summary Создать оборудование
     * @request POST:/api/v0/inventory-equipment/
     * @secure
     */
    v0InventoryEquipmentCreate: (
      data: InventoryEquipment,
      params: RequestParams = {},
    ) =>
      this.request<void, void>({
        path: `/api/v0/inventory-equipment/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **InventoryEquipmentStatus**. | Операция               | Требуемая permission | |------------------------|----------------------| | list / retrieve        | `view_inventoryequipmentstatus` | | create                 | `add_inventoryequipmentstatus` | | update / partial_update| `change_inventoryequipmentstatus` | | destroy                | `delete_inventoryequipmentstatus` |
     *
     * @tags v0
     * @name V0InventoryEquipmentStatusList
     * @summary Список статусов оборудования
     * @request GET:/api/v0/inventory-equipment-status/
     * @secure
     */
    v0InventoryEquipmentStatusList: (
      query?: {
        /** Номер страницы (≥ 1) */
        page?: number;
        /** Размер страницы (по умолчанию 20, максимум 100) */
        page_size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedInventoryEquipmentStatusList, any>({
        path: `/api/v0/inventory-equipment-status/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **InventoryEquipmentStatus**. | Операция               | Требуемая permission | |------------------------|----------------------| | list / retrieve        | `view_inventoryequipmentstatus` | | create                 | `add_inventoryequipmentstatus` | | update / partial_update| `change_inventoryequipmentstatus` | | destroy                | `delete_inventoryequipmentstatus` |
     *
     * @tags v0
     * @name V0InventoryEquipmentStatusCreate
     * @summary Создать статус
     * @request POST:/api/v0/inventory-equipment-status/
     * @secure
     */
    v0InventoryEquipmentStatusCreate: (
      data: InventoryEquipmentStatus,
      params: RequestParams = {},
    ) =>
      this.request<void, void>({
        path: `/api/v0/inventory-equipment-status/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **InventoryEquipmentStatus**. | Операция               | Требуемая permission | |------------------------|----------------------| | list / retrieve        | `view_inventoryequipmentstatus` | | create                 | `add_inventoryequipmentstatus` | | update / partial_update| `change_inventoryequipmentstatus` | | destroy                | `delete_inventoryequipmentstatus` |
     *
     * @tags v0
     * @name V0InventoryEquipmentStatusRetrieve
     * @summary Детали статуса
     * @request GET:/api/v0/inventory-equipment-status/{id}/
     * @secure
     */
    v0InventoryEquipmentStatusRetrieve: (
      id: number,
      params: RequestParams = {},
    ) =>
      this.request<InventoryEquipmentStatus, void>({
        path: `/api/v0/inventory-equipment-status/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **InventoryEquipmentStatus**. | Операция               | Требуемая permission | |------------------------|----------------------| | list / retrieve        | `view_inventoryequipmentstatus` | | create                 | `add_inventoryequipmentstatus` | | update / partial_update| `change_inventoryequipmentstatus` | | destroy                | `delete_inventoryequipmentstatus` |
     *
     * @tags v0
     * @name V0InventoryEquipmentStatusUpdate
     * @summary Полное обновление статуса
     * @request PUT:/api/v0/inventory-equipment-status/{id}/
     * @secure
     */
    v0InventoryEquipmentStatusUpdate: (
      id: number,
      data: InventoryEquipmentStatus,
      params: RequestParams = {},
    ) =>
      this.request<InventoryEquipmentStatus, any>({
        path: `/api/v0/inventory-equipment-status/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **InventoryEquipmentStatus**. | Операция               | Требуемая permission | |------------------------|----------------------| | list / retrieve        | `view_inventoryequipmentstatus` | | create                 | `add_inventoryequipmentstatus` | | update / partial_update| `change_inventoryequipmentstatus` | | destroy                | `delete_inventoryequipmentstatus` |
     *
     * @tags v0
     * @name V0InventoryEquipmentStatusPartialUpdate
     * @summary Частичное обновление статуса
     * @request PATCH:/api/v0/inventory-equipment-status/{id}/
     * @secure
     */
    v0InventoryEquipmentStatusPartialUpdate: (
      id: number,
      data: PatchedInventoryEquipmentStatus,
      params: RequestParams = {},
    ) =>
      this.request<InventoryEquipmentStatus, any>({
        path: `/api/v0/inventory-equipment-status/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **InventoryEquipmentStatus**. | Операция               | Требуемая permission | |------------------------|----------------------| | list / retrieve        | `view_inventoryequipmentstatus` | | create                 | `add_inventoryequipmentstatus` | | update / partial_update| `change_inventoryequipmentstatus` | | destroy                | `delete_inventoryequipmentstatus` |
     *
     * @tags v0
     * @name V0InventoryEquipmentStatusDestroy
     * @summary Удалить статус
     * @request DELETE:/api/v0/inventory-equipment-status/{id}/
     * @secure
     */
    v0InventoryEquipmentStatusDestroy: (
      id: number,
      params: RequestParams = {},
    ) =>
      this.request<void, any>({
        path: `/api/v0/inventory-equipment-status/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для **InventoryEquipment**. | Операция               | Model-permission | |------------------------|------------------| | list / retrieve        | `view_inventoryequipment` | | create                 | `add_inventoryequipment` | | update / partial_update| `change_inventoryequipment` | | destroy                | `delete_inventoryequipment` |
     *
     * @tags v0
     * @name V0InventoryEquipmentRetrieve
     * @summary Детали оборудования
     * @request GET:/api/v0/inventory-equipment/{id}/
     * @secure
     */
    v0InventoryEquipmentRetrieve: (id: number, params: RequestParams = {}) =>
      this.request<InventoryEquipment, void>({
        path: `/api/v0/inventory-equipment/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для **InventoryEquipment**. | Операция               | Model-permission | |------------------------|------------------| | list / retrieve        | `view_inventoryequipment` | | create                 | `add_inventoryequipment` | | update / partial_update| `change_inventoryequipment` | | destroy                | `delete_inventoryequipment` |
     *
     * @tags v0
     * @name V0InventoryEquipmentUpdate
     * @summary Полное обновление оборудования
     * @request PUT:/api/v0/inventory-equipment/{id}/
     * @secure
     */
    v0InventoryEquipmentUpdate: (
      id: number,
      data: InventoryEquipment,
      params: RequestParams = {},
    ) =>
      this.request<InventoryEquipment, any>({
        path: `/api/v0/inventory-equipment/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для **InventoryEquipment**. | Операция               | Model-permission | |------------------------|------------------| | list / retrieve        | `view_inventoryequipment` | | create                 | `add_inventoryequipment` | | update / partial_update| `change_inventoryequipment` | | destroy                | `delete_inventoryequipment` |
     *
     * @tags v0
     * @name V0InventoryEquipmentPartialUpdate
     * @summary Частичное обновление оборудования
     * @request PATCH:/api/v0/inventory-equipment/{id}/
     * @secure
     */
    v0InventoryEquipmentPartialUpdate: (
      id: number,
      data: PatchedInventoryEquipment,
      params: RequestParams = {},
    ) =>
      this.request<InventoryEquipment, any>({
        path: `/api/v0/inventory-equipment/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для **InventoryEquipment**. | Операция               | Model-permission | |------------------------|------------------| | list / retrieve        | `view_inventoryequipment` | | create                 | `add_inventoryequipment` | | update / partial_update| `change_inventoryequipment` | | destroy                | `delete_inventoryequipment` |
     *
     * @tags v0
     * @name V0InventoryEquipmentDestroy
     * @summary Удалить оборудование
     * @request DELETE:/api/v0/inventory-equipment/{id}/
     * @secure
     */
    v0InventoryEquipmentDestroy: (id: number, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/api/v0/inventory-equipment/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description Полноценный CRUD для *Location*. | Операция  | Требуемое model-permission | |-----------|---------------------------| | list / retrieve | `view_location` | | create | `add_location` | | update / partial_update | `change_location` | | destroy | `delete_location` |
     *
     * @tags v0
     * @name V0LocationList
     * @summary Список местоположений
     * @request GET:/api/v0/location/
     * @secure
     */
    v0LocationList: (
      query?: {
        /** Номер страницы (≥ 1) */
        page?: number;
        /** Размер страницы (по умолчанию 20, максимум 100) */
        page_size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedLocationList, any>({
        path: `/api/v0/location/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Полноценный CRUD для *Location*. | Операция  | Требуемое model-permission | |-----------|---------------------------| | list / retrieve | `view_location` | | create | `add_location` | | update / partial_update | `change_location` | | destroy | `delete_location` |
     *
     * @tags v0
     * @name V0LocationCreate
     * @summary Создать местоположение
     * @request POST:/api/v0/location/
     * @secure
     */
    v0LocationCreate: (data: Location, params: RequestParams = {}) =>
      this.request<void, void>({
        path: `/api/v0/location/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description Полноценный CRUD для *Location*. | Операция  | Требуемое model-permission | |-----------|---------------------------| | list / retrieve | `view_location` | | create | `add_location` | | update / partial_update | `change_location` | | destroy | `delete_location` |
     *
     * @tags v0
     * @name V0LocationRetrieve
     * @summary Детали местоположения
     * @request GET:/api/v0/location/{id}/
     * @secure
     */
    v0LocationRetrieve: (id: number, params: RequestParams = {}) =>
      this.request<Location, void>({
        path: `/api/v0/location/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description Полноценный CRUD для *Location*. | Операция  | Требуемое model-permission | |-----------|---------------------------| | list / retrieve | `view_location` | | create | `add_location` | | update / partial_update | `change_location` | | destroy | `delete_location` |
     *
     * @tags v0
     * @name V0LocationUpdate
     * @summary Полное обновление
     * @request PUT:/api/v0/location/{id}/
     * @secure
     */
    v0LocationUpdate: (
      id: number,
      data: Location,
      params: RequestParams = {},
    ) =>
      this.request<Location, any>({
        path: `/api/v0/location/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Полноценный CRUD для *Location*. | Операция  | Требуемое model-permission | |-----------|---------------------------| | list / retrieve | `view_location` | | create | `add_location` | | update / partial_update | `change_location` | | destroy | `delete_location` |
     *
     * @tags v0
     * @name V0LocationPartialUpdate
     * @summary Частичное обновление
     * @request PATCH:/api/v0/location/{id}/
     * @secure
     */
    v0LocationPartialUpdate: (
      id: number,
      data: PatchedLocation,
      params: RequestParams = {},
    ) =>
      this.request<Location, any>({
        path: `/api/v0/location/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description Полноценный CRUD для *Location*. | Операция  | Требуемое model-permission | |-----------|---------------------------| | list / retrieve | `view_location` | | create | `add_location` | | update / partial_update | `change_location` | | destroy | `delete_location` |
     *
     * @tags v0
     * @name V0LocationDestroy
     * @summary Удалить местоположение
     * @request DELETE:/api/v0/location/{id}/
     * @secure
     */
    v0LocationDestroy: (id: number, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/api/v0/location/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * No description
     *
     * @tags v0
     * @name V0LoginCreate
     * @request POST:/api/v0/login/
     * @secure
     */
    v0LoginCreate: (data: Login, params: RequestParams = {}) =>
      this.request<
        {
          detail?: string;
          user_id?: number;
          username?: string;
        },
        {
          detail?: string;
        }
      >({
        path: `/api/v0/login/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * No description
     *
     * @tags v0
     * @name V0LogoutCreate
     * @request POST:/api/v0/logout/
     * @secure
     */
    v0LogoutCreate: (params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/api/v0/logout/`,
        method: "POST",
        secure: true,
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для модели **Maintenance**. | Операция               | Требуемая permission                 | |------------------------|--------------------------------------| | list / retrieve        | `view_maintenance`                   | | create                 | `add_maintenance`                    | | update / partial_update| `change_maintenance`                 | | destroy                | `delete_maintenance`                 |
     *
     * @tags v0
     * @name V0MaintenanceList
     * @summary Список записей обслуживания оборудования
     * @request GET:/api/v0/maintenance/
     * @secure
     */
    v0MaintenanceList: (
      query?: {
        /** Номер страницы (≥ 1) */
        page?: number;
        /** Размер страницы (по умолчанию 20, максимум 100) */
        page_size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedMaintenanceList, any>({
        path: `/api/v0/maintenance/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для модели **Maintenance**. | Операция               | Требуемая permission                 | |------------------------|--------------------------------------| | list / retrieve        | `view_maintenance`                   | | create                 | `add_maintenance`                    | | update / partial_update| `change_maintenance`                 | | destroy                | `delete_maintenance`                 |
     *
     * @tags v0
     * @name V0MaintenanceCreate
     * @summary Создать новую запись обслуживания
     * @request POST:/api/v0/maintenance/
     * @secure
     */
    v0MaintenanceCreate: (data: Maintenance, params: RequestParams = {}) =>
      this.request<void, void>({
        path: `/api/v0/maintenance/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **MaintenanceStatus**. | Операция               | Требуемая permission                         | |------------------------|----------------------------------------------| | list / retrieve        | `view_maintenancestatus`                    | | create                 | `add_maintenancestatus`                     | | update / partial_update| `change_maintenancestatus`                  | | destroy                | `delete_maintenancestatus`                  |
     *
     * @tags v0
     * @name V0MaintenanceStatusList
     * @summary Список статусов обслуживания оборудования
     * @request GET:/api/v0/maintenance-status/
     * @secure
     */
    v0MaintenanceStatusList: (
      query?: {
        /** Номер страницы (≥ 1) */
        page?: number;
        /** Размер страницы (по умолчанию 20, максимум 100) */
        page_size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedMaintenanceStatusList, any>({
        path: `/api/v0/maintenance-status/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **MaintenanceStatus**. | Операция               | Требуемая permission                         | |------------------------|----------------------------------------------| | list / retrieve        | `view_maintenancestatus`                    | | create                 | `add_maintenancestatus`                     | | update / partial_update| `change_maintenancestatus`                  | | destroy                | `delete_maintenancestatus`                  |
     *
     * @tags v0
     * @name V0MaintenanceStatusCreate
     * @summary Создать статус обслуживания оборудования
     * @request POST:/api/v0/maintenance-status/
     * @secure
     */
    v0MaintenanceStatusCreate: (
      data: MaintenanceStatus,
      params: RequestParams = {},
    ) =>
      this.request<void, void>({
        path: `/api/v0/maintenance-status/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **MaintenanceStatus**. | Операция               | Требуемая permission                         | |------------------------|----------------------------------------------| | list / retrieve        | `view_maintenancestatus`                    | | create                 | `add_maintenancestatus`                     | | update / partial_update| `change_maintenancestatus`                  | | destroy                | `delete_maintenancestatus`                  |
     *
     * @tags v0
     * @name V0MaintenanceStatusRetrieve
     * @summary Детали статуса обслуживания оборудования
     * @request GET:/api/v0/maintenance-status/{id}/
     * @secure
     */
    v0MaintenanceStatusRetrieve: (id: number, params: RequestParams = {}) =>
      this.request<MaintenanceStatus, void>({
        path: `/api/v0/maintenance-status/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **MaintenanceStatus**. | Операция               | Требуемая permission                         | |------------------------|----------------------------------------------| | list / retrieve        | `view_maintenancestatus`                    | | create                 | `add_maintenancestatus`                     | | update / partial_update| `change_maintenancestatus`                  | | destroy                | `delete_maintenancestatus`                  |
     *
     * @tags v0
     * @name V0MaintenanceStatusUpdate
     * @summary Полное обновление статуса обслуживания оборудования
     * @request PUT:/api/v0/maintenance-status/{id}/
     * @secure
     */
    v0MaintenanceStatusUpdate: (
      id: number,
      data: MaintenanceStatus,
      params: RequestParams = {},
    ) =>
      this.request<MaintenanceStatus, any>({
        path: `/api/v0/maintenance-status/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **MaintenanceStatus**. | Операция               | Требуемая permission                         | |------------------------|----------------------------------------------| | list / retrieve        | `view_maintenancestatus`                    | | create                 | `add_maintenancestatus`                     | | update / partial_update| `change_maintenancestatus`                  | | destroy                | `delete_maintenancestatus`                  |
     *
     * @tags v0
     * @name V0MaintenanceStatusPartialUpdate
     * @summary Частичное обновление статуса обслуживания оборудования
     * @request PATCH:/api/v0/maintenance-status/{id}/
     * @secure
     */
    v0MaintenanceStatusPartialUpdate: (
      id: number,
      data: PatchedMaintenanceStatus,
      params: RequestParams = {},
    ) =>
      this.request<MaintenanceStatus, any>({
        path: `/api/v0/maintenance-status/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD эндпоинт для **MaintenanceStatus**. | Операция               | Требуемая permission                         | |------------------------|----------------------------------------------| | list / retrieve        | `view_maintenancestatus`                    | | create                 | `add_maintenancestatus`                     | | update / partial_update| `change_maintenancestatus`                  | | destroy                | `delete_maintenancestatus`                  |
     *
     * @tags v0
     * @name V0MaintenanceStatusDestroy
     * @summary Удалить статус обслуживания оборудования
     * @request DELETE:/api/v0/maintenance-status/{id}/
     * @secure
     */
    v0MaintenanceStatusDestroy: (id: number, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/api/v0/maintenance-status/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для модели **Maintenance**. | Операция               | Требуемая permission                 | |------------------------|--------------------------------------| | list / retrieve        | `view_maintenance`                   | | create                 | `add_maintenance`                    | | update / partial_update| `change_maintenance`                 | | destroy                | `delete_maintenance`                 |
     *
     * @tags v0
     * @name V0MaintenanceRetrieve
     * @summary Детали одной записи обслуживания
     * @request GET:/api/v0/maintenance/{id}/
     * @secure
     */
    v0MaintenanceRetrieve: (id: number, params: RequestParams = {}) =>
      this.request<Maintenance, void>({
        path: `/api/v0/maintenance/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для модели **Maintenance**. | Операция               | Требуемая permission                 | |------------------------|--------------------------------------| | list / retrieve        | `view_maintenance`                   | | create                 | `add_maintenance`                    | | update / partial_update| `change_maintenance`                 | | destroy                | `delete_maintenance`                 |
     *
     * @tags v0
     * @name V0MaintenanceUpdate
     * @summary Полное обновление записи обслуживания
     * @request PUT:/api/v0/maintenance/{id}/
     * @secure
     */
    v0MaintenanceUpdate: (
      id: number,
      data: Maintenance,
      params: RequestParams = {},
    ) =>
      this.request<Maintenance, any>({
        path: `/api/v0/maintenance/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для модели **Maintenance**. | Операция               | Требуемая permission                 | |------------------------|--------------------------------------| | list / retrieve        | `view_maintenance`                   | | create                 | `add_maintenance`                    | | update / partial_update| `change_maintenance`                 | | destroy                | `delete_maintenance`                 |
     *
     * @tags v0
     * @name V0MaintenancePartialUpdate
     * @summary Частичное обновление записи обслуживания
     * @request PATCH:/api/v0/maintenance/{id}/
     * @secure
     */
    v0MaintenancePartialUpdate: (
      id: number,
      data: PatchedMaintenance,
      params: RequestParams = {},
    ) =>
      this.request<Maintenance, any>({
        path: `/api/v0/maintenance/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD-эндпоинт для модели **Maintenance**. | Операция               | Требуемая permission                 | |------------------------|--------------------------------------| | list / retrieve        | `view_maintenance`                   | | create                 | `add_maintenance`                    | | update / partial_update| `change_maintenance`                 | | destroy                | `delete_maintenance`                 |
     *
     * @tags v0
     * @name V0MaintenanceDestroy
     * @summary Удалить запись обслуживания
     * @request DELETE:/api/v0/maintenance/{id}/
     * @secure
     */
    v0MaintenanceDestroy: (id: number, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/api/v0/maintenance/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description Регистрация нового пользователя. После успешного создания аккаунт помечается как `is_active=False` (это делает сам сериализатор)
     *
     * @tags v0
     * @name V0RegistrationCreate
     * @summary Регистрация пользователя
     * @request POST:/api/v0/registration/
     * @secure
     */
    v0RegistrationCreate: (
      data: UserRegistration,
      params: RequestParams = {},
    ) =>
      this.request<void, void>({
        path: `/api/v0/registration/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description Фильтры по полям `equipment`, `renter`, `assigned_by`, `location`. Поиск по описанию через `?search=`. Постраничная отдача.
     *
     * @tags v0
     * @name V0ReservationList
     * @summary Список бронирований
     * @request GET:/api/v0/reservation/
     * @secure
     */
    v0ReservationList: (
      query?: {
        assigned_by?: number;
        equipment?: number;
        location?: number;
        page?: number;
        page_size?: number;
        renter?: number;
        search?: string;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedReservationList, any>({
        path: `/api/v0/reservation/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD для модели Reservation (аренды оборудования). • list/retrieve — право `view_reservation` • create         — право `add_reservation` • update/patch   — право `change_reservation` • destroy        — право `delete_reservation`
     *
     * @tags v0
     * @name V0ReservationCreate
     * @summary Создать бронирование
     * @request POST:/api/v0/reservation/
     * @secure
     */
    v0ReservationCreate: (data: Reservation, params: RequestParams = {}) =>
      this.request<void, void>({
        path: `/api/v0/reservation/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description CRUD для модели Reservation (аренды оборудования). • list/retrieve — право `view_reservation` • create         — право `add_reservation` • update/patch   — право `change_reservation` • destroy        — право `delete_reservation`
     *
     * @tags v0
     * @name V0ReservationRetrieve
     * @summary Детали бронирования
     * @request GET:/api/v0/reservation/{id}/
     * @secure
     */
    v0ReservationRetrieve: (id: number, params: RequestParams = {}) =>
      this.request<Reservation, void>({
        path: `/api/v0/reservation/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD для модели Reservation (аренды оборудования). • list/retrieve — право `view_reservation` • create         — право `add_reservation` • update/patch   — право `change_reservation` • destroy        — право `delete_reservation`
     *
     * @tags v0
     * @name V0ReservationUpdate
     * @summary Полное обновление бронирования
     * @request PUT:/api/v0/reservation/{id}/
     * @secure
     */
    v0ReservationUpdate: (
      id: number,
      data: Reservation,
      params: RequestParams = {},
    ) =>
      this.request<Reservation, any>({
        path: `/api/v0/reservation/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD для модели Reservation (аренды оборудования). • list/retrieve — право `view_reservation` • create         — право `add_reservation` • update/patch   — право `change_reservation` • destroy        — право `delete_reservation`
     *
     * @tags v0
     * @name V0ReservationPartialUpdate
     * @summary Частичное обновление бронирования
     * @request PATCH:/api/v0/reservation/{id}/
     * @secure
     */
    v0ReservationPartialUpdate: (
      id: number,
      data: PatchedReservation,
      params: RequestParams = {},
    ) =>
      this.request<Reservation, any>({
        path: `/api/v0/reservation/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description CRUD для модели Reservation (аренды оборудования). • list/retrieve — право `view_reservation` • create         — право `add_reservation` • update/patch   — право `change_reservation` • destroy        — право `delete_reservation`
     *
     * @tags v0
     * @name V0ReservationDestroy
     * @summary Удалить бронирование
     * @request DELETE:/api/v0/reservation/{id}/
     * @secure
     */
    v0ReservationDestroy: (id: number, params: RequestParams = {}) =>
      this.request<void, any>({
        path: `/api/v0/reservation/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description **Полноценный CRUD для пользователей**. Доступ имеют: * суперпользователи; * члены групп **«Администратор системы»** или **«Модератор»**.
     *
     * @tags v0
     * @name V0UsersList
     * @summary Список пользователей
     * @request GET:/api/v0/users/
     * @secure
     */
    v0UsersList: (
      query?: {
        /** Номер страницы (≥ 1) */
        page?: number;
        /** Размер страницы (по умолчанию 20, максимум 100) */
        page_size?: number;
      },
      params: RequestParams = {},
    ) =>
      this.request<PaginatedUserList, void>({
        path: `/api/v0/users/`,
        method: "GET",
        query: query,
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description **Полноценный CRUD для пользователей**. Доступ имеют: * суперпользователи; * члены групп **«Администратор системы»** или **«Модератор»**.
     *
     * @tags v0
     * @name V0UsersCreate
     * @summary Создать пользователя
     * @request POST:/api/v0/users/
     * @secure
     */
    v0UsersCreate: (data: UserRegistration, params: RequestParams = {}) =>
      this.request<void, void>({
        path: `/api/v0/users/`,
        method: "POST",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),

    /**
     * @description **Полноценный CRUD для пользователей**. Доступ имеют: * суперпользователи; * члены групп **«Администратор системы»** или **«Модератор»**.
     *
     * @tags v0
     * @name V0UsersRetrieve
     * @summary Детальная информация о пользователе
     * @request GET:/api/v0/users/{id}/
     * @secure
     */
    v0UsersRetrieve: (id: number, params: RequestParams = {}) =>
      this.request<User, void>({
        path: `/api/v0/users/${id}/`,
        method: "GET",
        secure: true,
        format: "json",
        ...params,
      }),

    /**
     * @description **Полноценный CRUD для пользователей**. Доступ имеют: * суперпользователи; * члены групп **«Администратор системы»** или **«Модератор»**.
     *
     * @tags v0
     * @name V0UsersUpdate
     * @summary Полное обновление пользователя
     * @request PUT:/api/v0/users/{id}/
     * @secure
     */
    v0UsersUpdate: (id: number, data: User, params: RequestParams = {}) =>
      this.request<User, void>({
        path: `/api/v0/users/${id}/`,
        method: "PUT",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description **Полноценный CRUD для пользователей**. Доступ имеют: * суперпользователи; * члены групп **«Администратор системы»** или **«Модератор»**.
     *
     * @tags v0
     * @name V0UsersPartialUpdate
     * @summary Частичное обновление пользователя
     * @request PATCH:/api/v0/users/{id}/
     * @secure
     */
    v0UsersPartialUpdate: (
      id: number,
      data: PatchedUser,
      params: RequestParams = {},
    ) =>
      this.request<User, void>({
        path: `/api/v0/users/${id}/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        format: "json",
        ...params,
      }),

    /**
     * @description **Полноценный CRUD для пользователей**. Доступ имеют: * суперпользователи; * члены групп **«Администратор системы»** или **«Модератор»**.
     *
     * @tags v0
     * @name V0UsersDestroy
     * @summary Удалить пользователя
     * @request DELETE:/api/v0/users/{id}/
     * @secure
     */
    v0UsersDestroy: (id: number, params: RequestParams = {}) =>
      this.request<void, void>({
        path: `/api/v0/users/${id}/`,
        method: "DELETE",
        secure: true,
        ...params,
      }),

    /**
     * @description Позволяет включить или выключить пользователя. Требуются права `change_user` и принадлежность к разрешённой группе.
     *
     * @tags v0
     * @name V0UsersSetActivePartialUpdate
     * @summary Изменить флаг is_active
     * @request PATCH:/api/v0/users/{id}/set-active/
     * @secure
     */
    v0UsersSetActivePartialUpdate: (
      id: number,
      data: PatchedSetActive,
      params: RequestParams = {},
    ) =>
      this.request<void, void>({
        path: `/api/v0/users/${id}/set-active/`,
        method: "PATCH",
        body: data,
        secure: true,
        type: ContentType.Json,
        ...params,
      }),
  };
}
